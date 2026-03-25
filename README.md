# Sagnik Bhattacharya Website

<p align="center">
  <img src="public/sagnik-bhattacharya.png" alt="Sagnik Bhattacharya" width="180">
</p>

Public source for [sagnikbhattacharya.com](https://sagnikbhattacharya.com), a personal website and portfolio for Sagnik Bhattacharya, founder of Coding Liquids.

The site highlights:

- Courses in Flutter, Dart, and Excel with AI
- Corporate training and consulting services
- A blog with practical Excel, automation, and Flutter content
- Contact and profile pages for partnerships, training, and collaborations

## Stack

- Static HTML, CSS, and vanilla JavaScript
- Firebase Hosting for deployment
- GSAP and ScrollTrigger loaded via CDN for animations
- A PowerShell utility script for generating blog cover images and updating related metadata

There is no build step for the website itself. The deployable site lives directly inside [`public/`](public/).

## Project Structure

```text
.
|-- public/
|   |-- index.html
|   |-- about.html
|   |-- courses.html
|   |-- services.html
|   |-- blog.html
|   |-- contact.html
|   |-- blog/
|   |-- style.css
|   |-- animations.js
|   `-- assets, fonts, icons, and generated blog images
|-- scripts/
|   `-- sync-blog-covers.ps1
|-- firebase.json
`-- .firebaserc
```

## Local Development

Because this is a static site, you can preview it with any local web server.

### Option 1: Firebase Hosting Emulator

Prerequisite: install the Firebase CLI.

```bash
firebase emulators:start --only hosting
```

On Windows PowerShell, you may need:

```powershell
firebase.cmd emulators:start --only hosting
```

### Option 2: Serve the `public` folder directly

Use any static server you prefer and point it at `public/`.

Example with Python:

```bash
cd public
python -m http.server 8080
```

Note: Firebase clean URLs map `/about` to `about.html` in production. If you use a generic local server instead of the Firebase emulator, you may need to open `.html` routes directly.

## Deployment

This project is configured for Firebase Hosting with:

- `public` as the hosting root
- clean URLs enabled
- aggressive caching for static assets
- `no-cache` headers for HTML files

Deploy with:

```bash
firebase deploy --only hosting
```

The default Firebase project in [`.firebaserc`](.firebaserc) is `sagnik-bhattacharya`.

## Blog Cover Generation

[`scripts/sync-blog-covers.ps1`](scripts/sync-blog-covers.ps1) is a Windows PowerShell maintenance script that:

- regenerates blog cover images in `public/blog/images`
- updates Open Graph and Twitter image metadata in blog post HTML files
- updates JSON-LD image metadata
- injects cover images into blog post pages

Run it from the repository root with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-blog-covers.ps1
```

## Notes

- Primary site pages are plain `.html` files mapped to clean routes by Firebase Hosting.
- Styling is centralized in [`public/style.css`](public/style.css).
- Shared interactive behavior lives in [`public/animations.js`](public/animations.js).
- Blog posts are stored as individual HTML files inside [`public/blog/`](public/blog/).
