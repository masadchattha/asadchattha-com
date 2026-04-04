import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Mirrors the production `public/_headers` rule so the résumé behaves the same
// locally as on Cloudflare Pages: opens inline, and downloads with a proper
// filename instead of "resume.pdf".
const resumeHeaders = {
  name: 'resume-content-disposition',
  configureServer(server) {
    server.middlewares.use((req, res, next) => {
      if (req.url && req.url.split('?')[0].endsWith('/resume.pdf')) {
        res.setHeader(
          'Content-Disposition',
          'inline; filename="Muhammad_Asad_Senior_iOS_Engineer_CV.pdf"',
        );
      }
      next();
    });
  },
};

export default defineConfig({
  integrations: [
    tailwind({ applyBaseStyles: false }),
  ],
  vite: {
    plugins: [resumeHeaders],
  },
});
