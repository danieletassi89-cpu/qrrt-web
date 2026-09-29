# Strumenti UI per Claude Code

Stato in questo repo (PWA statica: `index.html`, `sw.js`, manifest).

## Già configurati
- **transitions.dev** – skill installata con `npx skills add Jakubantalik/transitions.dev` (`.claude/skills`, `.agents/skills`).
- **Agentation MCP** – server dichiarato in `.mcp.json` (`npx agentation-mcp server`).
  Il pacchetto npm `agentation` è per React: serve solo se il progetto passa a React.

## Da fare a mano (richiedono chiave personale, non committare mai la chiave)
- **OriginKit** – `claude mcp add originkit https://mcp.originkit.dev/mcp --transport http --header "Authorization: Bearer <API_KEY>" --scope user`
- **21st.dev** – `npx @21st-dev/cli@latest install claude` (API key gratuita su 21st.dev/mcp)

## Consultazione (nessuna installazione)
- **Aceternity UI** (ui.aceternity.com) – passa a Claude l'URL del componente scelto.
- **Component Gallery** (component.gallery) – consultala prima di creare un componente.

## Richiedono React (+ Tailwind per shadcn)
- **Beautiful UI** – `npx shadcn add https://www.beautifului.dev/r/registry.json`
- **Thinking Orbs** – `npm install thinking-orbs`
- **Agentation (libreria)** – `npm install agentation`
