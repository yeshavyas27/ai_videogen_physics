# Physica - AI Physics Video Generation

A chat-based interface for Physica, an AI engine that generates physics-accurate simulation videos.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Add your video:
   - Place your flood simulation video in `public/videos/`
   - Name it `flood-simulation.mp4` (or update the path in `src/App.tsx`)

3. Start the development server:
```bash
npm run dev
```

4. Open http://localhost:5173 in your browser

## Usage

Type a message asking for a "flood simulation" and Physica will display your pre-rendered video.

## Tech Stack

- React 18 + TypeScript
- Tailwind CSS
- Vite
- Lucide React (icons)

## Project Structure

```
src/
├── components/
│   ├── Header.tsx      # Navigation header
│   ├── ChatMessage.tsx # Message bubble component
│   ├── ChatInput.tsx   # Input field with send button
│   └── VideoPlayer.tsx # Video display component
├── App.tsx             # Main chat interface
├── types.ts            # TypeScript interfaces
└── index.css           # Global styles + Tailwind
```
