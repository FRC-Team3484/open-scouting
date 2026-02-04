import { defineConfig } from 'orval';

export default defineConfig({
    api: {
        output: {
            mode: 'tags-split',
            target: 'src/lib/api/api.ts',
            schemas: 'src/lib/api/model',
            client: 'fetch',
            mock: true,
            override: {
                mutator: {
                    path: 'src/lib/api/client.ts',
                    name: 'customInstance',
                }
            }
        },
        input: {
            target: 'http://localhost:8000/openapi.json',
        },
    },
});