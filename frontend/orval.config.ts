import { defineConfig } from 'orval';

export default defineConfig({
    api: {
        output: {
            mode: 'tags-split',
            target: 'src/lib/api/api.ts',
            schemas: 'src/lib/api/model',
            client: 'fetch',
            mock: false,
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
    zod: {
        output: {
            mode: 'tags-split',
            target: 'src/lib/zod/zod.ts',
            schemas: 'src/lib/zod/model',
            client: 'zod',
            mock: false,
        },
        input: {
            target: 'http://localhost:8000/openapi.json',
        },
    },
});