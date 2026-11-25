<template>
  <div class="min-h-screen bg-gray-50 py-24 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="font-display text-4xl sm:text-5xl text-gray-900 mb-4">Privacy Policy</h1>
        <p class="text-sm text-gray-400">Effective: June 1, 2025 &mdash; Last updated: June 1, 2025</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 sm:p-12 prose prose-gray max-w-none">
        <h2>1. General</h2>
        <p>This Privacy Policy describes how <strong>Lotus Studio</strong> (&ldquo;we,&rdquo; &ldquo;us,&rdquo; &ldquo;our&rdquo;) collects, uses, and protects the personal data of users (&ldquo;you,&rdquo; &ldquo;user&rdquo;) in connection with our games, services, and website.</p>
        <p>Our products are built on the <strong>Roblox</strong> platform using <strong>LuaU</strong>. By interacting with our games, you accept the terms of this policy.</p>
        <p><strong>Important:</strong> Our games run on the Roblox platform. Roblox Corporation has its own Privacy Policy governing data collection by the platform itself. We strongly recommend reviewing it at <a href="https://www.roblox.com/info/privacy" target="_blank">roblox.com</a>.</p>

        <h2>2. Data We Collect</h2>

        <h3>2.1 Data Received from Roblox</h3>
        <ul>
          <li><strong>Roblox User ID</strong> &mdash; a unique identifier within the Roblox system</li>
          <li><strong>Username</strong> &mdash; the in-game display name</li>
          <!-- <li><strong>Session statistics</strong> &mdash; time played, progress, achievements</li>
          <li><strong>Game transactions</strong> &mdash; in-game purchases via Robux</li> -->
        </ul>

        <h3>2.2 Technical Data</h3>
        <ul>
          <li>Game event logs (for debugging and gameplay improvement)</li>
          <li>Error and crash data</li>
          <li>Gameplay mechanic usage statistics</li>
        </ul>

        <h3>2.3 Data We Do <strong>Not</strong> Collect</h3>
        <ul>
          <li>Real name, surname, or date of birth</li>
          <li>Email address</li>
          <li>Phone number</li>
          <li>Payment data (all transactions are handled by PSP)</li>
          <li>IP address</li>
        </ul>

        <h2>3. How We Use Data</h2>
        <table>
          <thead>
            <tr><th>Purpose</th><th>Basis</th></tr>
          </thead>
          <tbody>
            <tr><td>Game functionality</td><td>Contract fulfillment</td></tr>
            <tr><td>Game progress saving</td><td>Legitimate interest</td></tr>
            <tr><td>Anti-cheat and enforcement</td><td>Legitimate interest / Security</td></tr>
            <tr><td>Gameplay balancing &amp; improvement</td><td>Legitimate interest</td></tr>
            <tr><td>Technical support</td><td>Contract fulfillment</td></tr>
          </tbody>
        </table>

        <h2>4. Children &amp; Minors</h2>
        <p>Roblox is a platform popular among minors. We take children&rsquo;s data protection seriously:</p>
        <ul>
          <li>We do not collect personally identifiable information from children</li>
          <li>We do not use minors&rsquo; data for advertising</li>
          <li>All purchases for users under 13 require parental confirmation (controlled by Roblox)</li>
          <li>Parents/guardians may contact us to request deletion of their child&rsquo;s data</li>
        </ul>

        <h2>5. Third-Party Data Sharing</h2>
        <p>We do <strong>not sell</strong> or <strong>share</strong> your data with third parties, except:</p>
        <ul>
          <li><strong>Roblox Corporation</strong> &mdash; as required for game functionality on the platform</li>
          <li><strong>Analytics services</strong> &mdash; in anonymized, aggregated form</li>
          <li><strong>Legal requirements</strong> &mdash; upon lawful government request</li>
        </ul>

        <h2>6. Data Storage &amp; Security</h2>
        <ul>
          <li>Game data is stored in <strong>Roblox DataStore</strong> &mdash; Roblox&rsquo;s secure storage system</li>
          <li>Data is retained only as long as necessary for its function</li>
          <li>When a Roblox account is deleted, associated data becomes inaccessible to us</li>
        </ul>

        <h2>7. Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
          <li><strong>Request information</strong> about stored data</li>
          <li><strong>Request deletion</strong> of your data</li>
          <li><strong>Object to processing</strong> in certain cases</li>
          <li><strong>File a complaint</strong> with your country&rsquo;s data protection authority</li>
        </ul>
        <p>To exercise your rights, contact us at: <strong>####</strong></p>

        <h2>8. Policy Changes</h2>
        <p>We may update this policy. For material changes, we will notify users via in-game notifications or announcements in the Roblox group. Continued use of our games constitutes acceptance of the updated policy.</p>

        <h2>9. Contact</h2>
        <p>
          <strong>Lotus Studio</strong><br />
          Email: ####<br />
          Roblox Group: <a href="https://www.roblox.com/share/g/32638472" target="_blank">Lotus Studio Group</a><br />
          Discord: <a href="https://discord.gg/YAC8Vsra" target="_blank">discord.gg/lotusstudio</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Privacy Policy — Lotus Studio',
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
.prose a { @apply text-teal-600 hover:text-teal-700; }
.prose hr { @apply my-8 border-gray-200; }
</style>
