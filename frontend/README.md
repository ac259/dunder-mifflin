# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```

### What is Vite?  *<context> to self*
Vite (pronounced "veet") is a modern frontend build tool that makes starting and developing React (or other JavaScript frameworks) super fast.

It replaces older tools like Create React App (CRA), which are slower and more complex.

### Why Use Vite Instead of Create React App (CRA)?
Here are the main reasons why Vite is better:

1️⃣ Faster Startup 🚀

CRA bundles everything before starting, which takes time.
Vite instantly starts your app without bundling everything upfront.
2️⃣ Instant Hot Reloading ⚡

In CRA, when you change code, it recompiles everything (slow).
In Vite, it reloads only what changed (super fast).
3️⃣ Lightweight & Minimal 🏋️‍♂️

CRA includes a lot of extra files you might not need.
Vite is leaner and gives you just what’s necessary.
4️⃣ Better for Production 📦

Vite uses esbuild, a modern JavaScript bundler, making builds much faster.
CRA’s build process is slower and sometimes bloated.
