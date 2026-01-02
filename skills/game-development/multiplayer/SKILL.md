---
name: multiplayer
description: Multiplayer game networking patterns and architecture. Use when implementing real-time multiplayer, matchmaking, synchronization, lag compensation, or dedicated servers.
---

# Multiplayer Game Development

> Networking patterns for real-time and turn-based multiplayer games

## Architecture Types

| Type | Latency | Use Case |
|------|---------|----------|
| **Client-Server** | 50-150ms | Competitive, authoritative |
| **P2P** | Variable | Co-op, fighting games |
| **Relay** | Higher | NAT traversal, fallback |
| **Dedicated** | Lowest | Esports, MMOs |

---

## Client-Server Architecture

### Authoritative Server
```
Client: "I want to move forward"
Server: Validates → Updates → Broadcasts
Client: Receives authoritative state

Never trust the client:
- Validate all actions
- Server owns game state
- Client predicts, server corrects
```

### State Synchronization
```typescript
// Snapshot interpolation
const BUFFER_SIZE = 3; // frames
const snapshots: Snapshot[] = [];

function render(currentTime: number) {
    const renderTime = currentTime - INTERPOLATION_DELAY;
    const [before, after] = findSnapshots(renderTime);
    const t = (renderTime - before.time) / (after.time - before.time);
    
    // Interpolate positions
    entity.position = lerp(before.position, after.position, t);
}
```

---

## Lag Compensation

### Client-Side Prediction
```typescript
// Predict locally, reconcile with server
class PredictedMovement {
    private pendingInputs: Input[] = [];
    private sequence = 0;
    
    processInput(input: Input) {
        // Apply locally immediately
        this.applyInput(input);
        
        // Send to server
        input.sequence = this.sequence++;
        this.pendingInputs.push(input);
        network.send(input);
    }
    
    reconcile(serverState: State) {
        // Remove acknowledged inputs
        this.pendingInputs = this.pendingInputs
            .filter(i => i.sequence > serverState.lastSequence);
        
        // Re-apply pending inputs
        this.position = serverState.position;
        for (const input of this.pendingInputs) {
            this.applyInput(input);
        }
    }
}
```

### Server Reconciliation
```
Client tick: 16ms (60fps)
Server tick: 20-33ms (30-50fps)
Network delay: Variable

Timeline:
  Client t=100: Input sent
  Server t=120: Input received, processed
  Client t=150: State update received
  Client: Reconcile with pending inputs
```

---

## WebSocket Implementation

### Real-Time Protocol
```typescript
// Client
const ws = new WebSocket('wss://game-server.example.com');

ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'join', room: 'lobby' }));
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    
    switch (msg.type) {
        case 'state': updateGameState(msg.data); break;
        case 'playerJoin': addPlayer(msg.player); break;
        case 'playerLeave': removePlayer(msg.playerId); break;
    }
};

// Send input (throttled to tick rate)
function sendInput(input: InputData) {
    ws.send(JSON.stringify({ type: 'input', data: input }));
}
```

### Binary Protocol (Performance)
```typescript
// More efficient for real-time games
const buffer = new ArrayBuffer(12);
const view = new DataView(buffer);

view.setUint8(0, MessageType.POSITION);
view.setFloat32(1, x, true);
view.setFloat32(5, y, true);
view.setUint16(9, sequence, true);

ws.send(buffer);
```

---

## Unity Netcode

### Netcode for GameObjects
```csharp
public class PlayerController : NetworkBehaviour
{
    [ServerRpc]
    private void MoveServerRpc(Vector3 direction)
    {
        // Server validates and applies
        transform.position += direction * speed * Time.deltaTime;
    }
    
    [ClientRpc]
    private void PlayEffectClientRpc(Vector3 position)
    {
        // All clients play effect
        Instantiate(effectPrefab, position, Quaternion.identity);
    }
    
    void Update()
    {
        if (IsOwner)
        {
            var input = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
            MoveServerRpc(input);
        }
    }
}
```

### Network Variables
```csharp
public NetworkVariable<int> Health = new NetworkVariable<int>(100);
public NetworkVariable<Vector3> Position = new NetworkVariable<Vector3>();

void Awake()
{
    Health.OnValueChanged += (prev, current) => {
        UpdateHealthUI(current);
    };
}
```

---

## Godot Multiplayer

### High-Level Multiplayer
```gdscript
extends Node

func _ready() -> void:
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)

func host_game() -> void:
    var peer = ENetMultiplayerPeer.new()
    peer.create_server(7777, 4)  # port, max_clients
    multiplayer.multiplayer_peer = peer

func join_game(ip: String) -> void:
    var peer = ENetMultiplayerPeer.new()
    peer.create_client(ip, 7777)
    multiplayer.multiplayer_peer = peer

@rpc("any_peer", "call_local", "reliable")
func player_moved(pos: Vector2) -> void:
    var sender_id = multiplayer.get_remote_sender_id()
    players[sender_id].position = pos
```

---

## Matchmaking

### Implementation
```typescript
interface MatchRequest {
    playerId: string;
    skill: number;  // ELO/MMR
    preferences: {
        gameMode: string;
        region: string;
    };
}

class Matchmaker {
    private queue: MatchRequest[] = [];
    
    findMatch(request: MatchRequest): Match | null {
        // Find players within skill range
        const skillRange = 200;
        const candidates = this.queue.filter(r => 
            Math.abs(r.skill - request.skill) < skillRange &&
            r.preferences.region === request.preferences.region
        );
        
        if (candidates.length >= PLAYERS_NEEDED - 1) {
            return this.createMatch([request, ...candidates.slice(0, PLAYERS_NEEDED - 1)]);
        }
        
        this.queue.push(request);
        return null;
    }
}
```

---

## Anti-Cheat Basics

### Server-Side Validation
```
Always validate:
- Movement speed (max delta per tick)
- Cooldowns (can't spam abilities)
- Line of sight (can player see target?)
- Resource limits (can't have more than earned)
- Action sequences (proper state transitions)
```

### Common Cheats to Prevent
| Cheat | Prevention |
|-------|------------|
| Speed hack | Server validates movement delta |
| Teleport | Position changes require time |
| Wallhack | Only send visible entities |
| Aimbot | Server-side hit validation |
| Duplicate items | Authoritative inventory |

---

## Performance Tips

```
Bandwidth optimization:
- Delta compression (only send changes)
- Prioritize nearby entities
- Lower tick rate for distant objects
- Binary protocol (not JSON)

Latency hiding:
- Client prediction
- Interpolation buffer
- Audio/visual effects predict ahead
- Forgiving hit detection
```
