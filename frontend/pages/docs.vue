<template>
  <div class="min-h-screen bg-gray-50 py-24 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="font-display text-4xl sm:text-5xl text-gray-900 mb-4">Documentation</h1>
        <p class="text-lg text-gray-500">Roblox LuaU development, testing & game sales guide</p>
        <p class="text-sm text-gray-400 mt-1">V 1.7 &mdash; Platform: Roblox &mdash; Language: LuaU (Luau)</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 sm:p-12 prose prose-gray max-w-none">
        <h2>Table of Contents</h2>
        <ol>
          <li><a href="#project-structure">Project Structure</a></li>
          <li><a href="#lua-standards">LuaU Code Standards</a></li>
          <li><a href="#game-architecture">Game Architecture</a></li>
          <li><a href="#development-process">Development Process</a></li>
          <li><a href="#testing">Testing</a></li>
          <li><a href="#datastore">DataStore</a></li>
          <li><a href="#monetization">Monetization &amp; Robux</a></li>
          <li><a href="#publishing">Publishing &amp; Selling</a></li>
          <li><a href="#security">Security &amp; Anti-Cheat</a></li>
          <li><a href="#support">Support &amp; Bug Reports</a></li>
        </ol>

        <hr />

        <h2 id="project-structure">1. Project Structure</h2>
        <p>Recommended file structure inside <strong>Roblox Studio</strong> (via Rojo or directly):</p>
        <pre><code>game/
&tilde;/ ServerScriptService/
&tilde; &tilde;/ Core/
&tilde; &tilde; &tilde;/ GameManager.server.luau     -- Game initialization
&tilde; &tilde; &tilde;/ DataManager.server.luau     -- DataStore operations
&tilde; &tilde; &tilde;/ AntiCheat.server.luau       -- Server-side protection
&tilde; &tilde;/ Systems/
&tilde; &tilde; &tilde;/ CombatSystem.server.luau
&tilde; &tilde; &tilde;/ EconomySystem.server.luau
&tilde; /
&tilde;/ ReplicatedStorage/
&tilde; &tilde;/ Modules/
&tilde; &tilde; &tilde;/ SharedTypes.luau            -- Shared types (TypeChecking)
&tilde; &tilde; &tilde;/ Constants.luau              -- Game constants
&tilde; &tilde; &tilde;/ Utilities.luau             -- Utilities
&tilde; &tilde;/ RemoteEvents/                   -- RemoteEvent / RemoteFunction
&tilde; /
&tilde;/ StarterPlayerScripts/
&tilde; &tilde;/ UI/
&tilde; &tilde; &tilde;/ HUDController.client.luau
&tilde; &tilde; &tilde;/ ShopController.client.luau
&tilde; &tilde;/ Input/
&tilde; &tilde; &tilde;/ InputHandler.client.luau
&tilde; /
&tilde;/ StarterGui/
&tilde; &tilde;/ [UI components]</code></pre>

        <h2 id="lua-standards">2. LuaU Code Standards</h2>

        <h3>2.1 Naming Conventions</h3>
        <table>
          <thead>
            <tr><th>Entity</th><th>Style</th><th>Example</th></tr>
          </thead>
          <tbody>
            <tr><td>Variables</td><td>camelCase</td><td><code>playerData</code>, <code>maxHealth</code></td></tr>
            <tr><td>Functions</td><td>camelCase</td><td><code>getPlayerLevel()</code></td></tr>
            <tr><td>Constants</td><td>UPPER_SNAKE_CASE</td><td><code>MAX_PLAYERS</code>, <code>SPAWN_DELAY</code></td></tr>
            <tr><td>Classes/Modules</td><td>PascalCase</td><td><code>DataManager</code>, <code>CombatSystem</code></td></tr>
            <tr><td>Private fields</td><td><code>_</code> prefix</td><td><code>_internalState</code></td></tr>
          </tbody>
        </table>

        <h3>2.2 Type Checking</h3>
        <p>Always use strict typing (<code>--!strict</code>):</p>
        <pre><code>--!strict

type PlayerData = {
&tilde; userId: number,
&tilde; coins: number,
&tilde; level: number,
&tilde; inventory: {string},
&tilde; lastLogin: number,
}

local function createPlayer(userId: number, name: string): PlayerData
&tilde; return {
&tilde; &tilde; userId = userId,
&tilde; &tilde; coins = 0,
&tilde; &tilde; level = 1,
&tilde; &tilde; inventory = {},
&tilde; &tilde; lastLogin = os.time(),
&tilde; }
end</code></pre>

        <h3>2.3 Module Pattern</h3>
        <pre><code>-- Modules/CombatSystem.luau
local CombatSystem = {}
CombatSystem.__index = CombatSystem

type CombatSystemType = {
&tilde; damage: number,
&tilde; attackPlayer: (self: CombatSystemType, target: Player) -> (),
}

function CombatSystem.new(damage: number): CombatSystemType
&tilde; local self = setmetatable({}, CombatSystem)
&tilde; self.damage = damage
&tilde; return self :: CombatSystemType
end

function CombatSystem:attackPlayer(target: Player)
&tilde; -- attack logic
end

return CombatSystem</code></pre>

        <h3>2.4 RemoteEvents</h3>
        <p><strong>Server → Client:</strong></p>
        <pre><code>-- Server
local remoteEvent = game.ReplicatedStorage.RemoteEvents.UpdateCoins
remoteEvent:FireClient(player, newCoinAmount)

-- Client
remoteEvent.OnClientEvent:Connect(function(amount: number)
&tilde; updateCoinUI(amount)
end)</code></pre>

        <p><strong>Client → Server (with validation):</strong></p>
        <pre><code>-- Client
local buyItemEvent = game.ReplicatedStorage.RemoteEvents.BuyItem
buyItemEvent:FireServer(itemId)

-- Server — ALWAYS validate client data
buyItemEvent.OnServerEvent:Connect(function(player: Player, itemId: unknown)
&tilde; -- Type validation
&tilde; if type(itemId) ~= "string" then return end
&tilde; -- Value validation
&tilde; if not VALID_ITEMS[itemId] then return end
&tilde; -- Purchase logic
&tilde; processPurchase(player, itemId)
end)</code></pre>

        <h2 id="game-architecture">3. Game Architecture</h2>

        <h3>3.1 Client-Server Model</h3>
        <pre><code>+-----------------------------------------------------+
|                      SERVER                         |
|  +---------------+  +--------------+  +-----------+  |
|  | GameManager   |  | DataManager  |  | AntiCheat |  |
|  +-------+-------+  +------+-------+  +-----+-----+  |
|          +------------------+------------------+      |
|                      RemoteEvents                      |
+---------------------------+---------------------------+
                            | Network (secure channel)
+---------------------------+---------------------------+
|                      CLIENT                         |
|  +---------------+  +--------------+                 |
|  | HUDController |  |InputHandler  |                 |
|  +---------------+  +--------------+                 |
+-----------------------------------------------------+</code></pre>
        <p><strong>Rule:</strong> All gameplay logic affecting progress and economy runs <strong>only on the server</strong>.</p>

        <h2 id="development-process">4. Development Process</h2>

        <h3>4.1 Workflow (Git + Rojo)</h3>
        <pre><code># Install Rojo
aftman install

# Sync project
rojo serve default.project.json

# Branch structure
main          -- stable version
develop       -- active development
feature/*     -- new features
hotfix/*      -- urgent fixes</code></pre>

        <h3>4.2 Development Stages</h3>
        <table>
          <thead>
            <tr><th>Stage</th><th>Description</th><th>Result</th></tr>
          </thead>
          <tbody>
            <tr><td>Prototype</td><td>Core mechanics, no assets</td><td>Playable prototype</td></tr>
            <tr><td>Alpha</td><td>All mechanics, placeholder assets</td><td>Internal testing</td></tr>
            <tr><td>Beta</td><td>Final assets, balancing</td><td>Closed beta testing</td></tr>
            <tr><td>Release</td><td>Publishing, monitoring</td><td>Public access</td></tr>
            <tr><td>Support</td><td>Updates, fixes</td><td>Patches &amp; content</td></tr>
          </tbody>
        </table>

        <h2 id="testing">5. Testing</h2>

        <h3>5.1 Unit Testing</h3>
        <pre><code>-- Tests/DataManager.spec.luau
local DataManager = require(game.ServerScriptService.Core.DataManager)

local function testCreateProfile()
&tilde; local profile = DataManager.createProfile(12345)
&tilde; assert(profile.coins == 0, "Starting coins should be 0")
&tilde; assert(profile.level == 1, "Starting level should be 1")
&tilde; print("PASSED: testCreateProfile")
end

testCreateProfile()</code></pre>

        <h3>5.2 Pre-Release Checklist</h3>
        <ul>
          <li>All RemoteEvent data validated server-side</li>
          <li>DataStore wrapped in pcall with error handling</li>
          <li>No infinite loops without task.wait()</li>
          <li>Performance verified (&lt; 16ms server frametime)</li>
          <li>Disconnected player handling</li>
          <li>Tested with 20+ concurrent players</li>
          <li>No memory leaks</li>
          <li>All texts passed Roblox moderation</li>
        </ul>

        <h3>5.3 Debugging Tools</h3>
        <pre><code>-- Performance profiling
debug.profilebegin("CombatSystem:update")
-- ... code ...
debug.profileend()

-- Logging
local function log(level: "INFO" | "WARN" | "ERROR", message: string)
&tilde; if level == "ERROR" then
&tilde; &tilde; warn(string.format("[ERROR] %s", message))
&tilde; elseif level == "WARN" then
&tilde; &tilde; warn(string.format("[WARN] %s", message))
&tilde; else
&tilde; &tilde; print(string.format("[INFO] %s", message))
&tilde; end
end</code></pre>

        <h2 id="datastore">6. DataStore</h2>

        <h3>6.1 Safe DataStore Operations</h3>
        <pre><code>--!strict
local DataStoreService = game:GetService("DataStoreService")
local playerDataStore = DataStoreService:GetDataStore("PlayerData_v1")

type PlayerData = {
&tilde; coins: number,
&tilde; level: number,
&tilde; inventory: {string},
}

local DEFAULT_DATA: PlayerData = {
&tilde; coins = 100,
&tilde; level = 1,
&tilde; inventory = {},
}

local function loadPlayerData(userId: number): PlayerData
&tilde; local success, result = pcall(function()
&tilde; &tilde; return playerDataStore:GetAsync(tostring(userId))
&tilde; end)
&tilde; if success and result then
&tilde; &tilde; for key, value in DEFAULT_DATA do
&tilde; &tilde; &tilde; if result[key] == nil then result[key] = value end
&tilde; &tilde; end
&tilde; &tilde; return result
&tilde; end
&tilde; return table.clone(DEFAULT_DATA)
end

local function savePlayerData(userId: number, data: PlayerData): boolean
&tilde; local success, err = pcall(function()
&tilde; &tilde; playerDataStore:SetAsync(tostring(userId), data)
&tilde; end)
&tilde; if not success then
&tilde; &tilde; warn("DataStore save error for", userId, ":", err)
&tilde; end
&tilde; return success
end</code></pre>

        <h2 id="monetization">7. Monetization &amp; Robux</h2>

        <h3>7.1 Game Passes</h3>
        <pre><code>local MarketplaceService = game:GetService("MarketplaceService")

local GAME_PASSES = {
&tilde; VIP = 123456789,
&tilde; DOUBLE_XP = 987654321,
}

local function checkGamePasses(player: Player)
&tilde; for passName, passId in GAME_PASSES do
&tilde; &tilde; local success, hasPass = pcall(function()
&tilde; &tilde; &tilde; return MarketplaceService:UserOwnsGamePassAsync(player.UserId, passId)
&tilde; &tilde; end)
&tilde; &tilde; if success and hasPass then
&tilde; &tilde; &tilde; applyPassBenefit(player, passName)
&tilde; &tilde; end
&tilde; end
end</code></pre>

        <h3>7.2 Developer Products</h3>
        <pre><code>MarketplaceService.ProcessReceipt = function(receiptInfo)
&tilde; local player = game.Players:GetPlayerByUserId(receiptInfo.PlayerId)
&tilde; if not player then
&tilde; &tilde; return Enum.ProductPurchaseDecision.NotProcessedYet
&tilde; end
&tilde; local PRODUCTS = {
&tilde; &tilde; [111111111] = function() giveCoins(player, 1000) end,
&tilde; &tilde; [222222222] = function() giveCoins(player, 5000) end,
&tilde; }
&tilde; local handler = PRODUCTS[receiptInfo.ProductId]
&tilde; if handler then
&tilde; &tilde; local success = pcall(handler)
&tilde; &tilde; if success then
&tilde; &tilde; &tilde; return Enum.ProductPurchaseDecision.PurchaseGranted
&tilde; &tilde; end
&tilde; end
&tilde; return Enum.ProductPurchaseDecision.NotProcessedYet
end</code></pre>

        <h2 id="publishing">8. Publishing &amp; Selling</h2>

        <h3>8.1 Pre-Publication Checklist</h3>
        <ul>
          <li>Game settings: title, description, icon, screenshots (800&times;450 px)</li>
          <li>Genre and age rating set correctly</li>
          <li>Tested on mobile devices</li>
          <li>Server Fill: Fill Server / VIP Servers configured</li>
          <li>Social links (Discord, Group) added</li>
          <li>Place file updated to latest version</li>
        </ul>

        <h3>8.2 Selling a Completed Game</h3>
        <table>
          <thead>
            <tr><th>Artifact</th><th>Format</th><th>Description</th></tr>
          </thead>
          <tbody>
            <tr><td>Source code</td><td>.rbxl / Git repo</td><td>Full project with history</td></tr>
            <tr><td>Documentation</td><td>Markdown / PDF</td><td>This file + README</td></tr>
            <tr><td>Assets</td><td>Roblox Asset IDs</td><td>List of all uploaded assets</td></tr>
            <tr><td>DataStore schema</td><td>JSON schema</td><td>Stored data structure</td></tr>
            <tr><td>Rights transfer</td><td>Contract</td><td>Written agreement</td></tr>
          </tbody>
        </table>
        <p><strong>Note:</strong> After transfer, the buyer is responsible for Roblox ToS compliance.</p>

        <h2 id="security">9. Security &amp; Anti-Cheat</h2>

        <h3>9.1 Core Rules</h3>
        <ol>
          <li><strong>Never trust the client</strong> &mdash; all critical checks on the server</li>
          <li><strong>Validate types and ranges</strong> of all RemoteEvent arguments</li>
          <li><strong>Rate limiting</strong> &mdash; throttle events per player</li>
          <li><strong>String sanitization</strong> &mdash; don't inject user input into commands</li>
        </ol>

        <pre><code>-- Rate limiter
local rateLimits: {[number]: number} = {}
local RATE_LIMIT_SECONDS = 0.5

local function isRateLimited(userId: number): boolean
&tilde; local now = os.clock()
&tilde; local last = rateLimits[userId] or 0
&tilde; if now - last &lt; RATE_LIMIT_SECONDS then return true end
&tilde; rateLimits[userId] = now
&tilde; return false
end</code></pre>

        <h3>9.2 Cheat Detection</h3>
        <pre><code>-- Player speed validation (server-side)
local function validatePlayerSpeed(player: Player, reportedPosition: Vector3)
&tilde; local character = player.Character
&tilde; if not character then return end
&tilde; local rootPart = character:FindFirstChild("HumanoidRootPart") :: BasePart
&tilde; if not rootPart then return end
&tilde; local maxSpeed = getPlayerMaxSpeed(player)
&tilde; local distance = (rootPart.Position - reportedPosition).Magnitude
&tilde; if distance &gt; maxSpeed * 2 then
&tilde; &tilde; warn("Possible speedhack:", player.Name)
&tilde; end
end</code></pre>

        <h2 id="support">10. Support &amp; Bug Reports</h2>

        <h3>10.1 Support Channels</h3>
        <table>
          <thead>
            <tr><th>Channel</th><th>Purpose</th><th>Response Time</th></tr>
          </thead>
          <tbody>
            <tr><td>Discord #bug-reports</td><td>Bugs, glitches</td><td>24&ndash;48 h</td></tr>
            <tr><td>Discord #support</td><td>Player questions</td><td>24&ndash;72 h</td></tr>
            <tr><td>Email</td><td>Business inquiries</td><td>3&ndash;5 business days</td></tr>
            <tr><td>Roblox DevForum</td><td>Technical questions</td><td>Public</td></tr>
          </tbody>
        </table>

        <h3>10.2 Bug Report Template</h3>
        <pre><code>**Game Title:**
**Version (PlaceId):**
**Bug Description:**
**Steps to Reproduce:**
&tilde; 1.
&tilde; 2.
&tilde; 3.
**Expected Behavior:**
**Actual Behavior:**
**Screenshot/Video:** [attach]
**Platform:** PC / Mobile / Console
**Date &amp; Time:**</code></pre>

        <hr />
        <p class="text-sm text-gray-400">Documentation maintained by Lotus Studio. For questions: <a href="/support">Help Center</a> or Discord.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Documentation — Lotus Studio',
})
</script>

<style scoped>
.prose h2 { @apply font-display text-2xl text-gray-900 mt-12 mb-4; }
.prose h3 { @apply font-display text-xl text-gray-900 mt-8 mb-3; }
.prose p { @apply text-gray-600 leading-relaxed mb-4; }
.prose ul, .prose ol { @apply text-gray-600 mb-4 pl-6; }
.prose li { @apply mb-1; }
.prose table { @apply w-full text-sm text-gray-600 mb-6; }
.prose th { @apply text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-4 py-3 bg-gray-50; }
.prose td { @apply px-4 py-3 border-t border-gray-100; }
.prose pre { @apply bg-gray-900 text-gray-100 rounded-xl p-4 mb-6 overflow-x-auto text-sm leading-relaxed; }
.prose code { @apply text-teal-300; }
.prose hr { @apply my-8 border-gray-200; }
.prose a { @apply text-teal-600 hover:text-teal-700; }
</style>
