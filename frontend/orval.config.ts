import { defineConfig } from 'orval';

export default defineConfig({
    api: {
        output: {
            mode: 'tags-split',
            target: 'src/api/api.ts',
            schemas: 'src/api/model',
            client: 'svelte-query',
            mock: true,
        },
        input: {
            target: 'http://localhost:8000/openapi.json',
        },
    },
});