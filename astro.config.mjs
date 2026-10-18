import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";
export default defineConfig({
  devToolbar: { enabled: false },
  adapter: cloudflare()
});