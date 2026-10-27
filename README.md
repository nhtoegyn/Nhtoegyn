# Project Aether — 3D Multiplayer Starter (Godot 4.7.x)

A small learning prototype with a procedural 3D field, an orthographic isometric-style camera, simple placeholder player models, and server-authoritative grid movement over ENet/UDP.

## Important limitations

This is a prototype, not a secure or production-ready MMORPG server. It has no accounts, persistence, encryption, anti-cheat system, rate limiting, moderation tools, or database. Do not expose a long-running public game server to the internet for real players yet.

## Windows quick start

Extract this folder to `C:\Games\ProjectAether3D` (or another path). Open PowerShell in the project folder.

### 1. Start the server

```powershell
& "C:\Godot\Godot_v4.7.2-stable_win64_console.exe" --path "C:\Games\ProjectAether3D" -- --server
```

### 2. Start a client on the same PC

In a second PowerShell window:

```powershell
& "C:\Godot\Godot_v4.7.2-stable_win64.exe" --path "C:\Games\ProjectAether3D" -- --connect=127.0.0.1
```

Adjust the executable and project paths to match your PC. If you only have the console executable, you can also try it for the client, but the normal executable is better for a graphical game.

## Internet testing (only after local test works)

ENet uses UDP. To test from outside your home network, the host needs a public reachable IPv4 address (or another supported network setup), a router port-forward for **UDP 2456** to the server PC, and a Windows Firewall inbound rule for UDP 2456. The remote client uses:

```powershell
& "C:\Godot\Godot_v4.7.2-stable_win64.exe" --path "C:\Games\ProjectAether3D" -- --connect=YOUR_PUBLIC_IP
```

Never share your public IP in a public chat. Some ISPs use CGNAT, which prevents ordinary port forwarding. In that case use a VPS or a VPN/overlay network for testing. For an eventual commercial game, prefer a managed/dedicated server instead of hosting on your personal PC.

## Controls

- WASD or arrow keys: move one grid step at a time.

## Suggested next milestones

1. Confirm two clients see each other locally.
2. Test over a private network / VPS.
3. Add proper 3D character assets and animations.
4. Add collision/navigation, combat, NPCs and persistence.
5. Only then design accounts, database, security and deployment.
