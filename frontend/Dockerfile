# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
ENV NODE_OPTIONS=--max-old-space-size=4096

# Set dummy .env values so node build doesn't fail
ENV PUBLIC_FAST_API_URL=https://open-scouting.shortcircuitfirst.org
ENV PUBLIC_FRONTEND_URL=https://open-scouting.shortcircuitfirst.org
ENV PUBLIC_EMAIL_ENABLED=false
ENV PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES=15

COPY package*.json ./

RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "build/index.js"]