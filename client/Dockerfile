# Build stage
FROM node:24-alpine as builder

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build the app
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
RUN pnpm build

# Production stage
FROM node:24-alpine

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/pnpm-lock.yaml ./pnpm-lock.yaml

# Install production dependencies only
RUN npm install -g pnpm && \
    pnpm install --prod --frozen-lockfile

# Set environment variables
ENV VITE_API_URL=${VITE_API_URL}

EXPOSE 3000

CMD ["node", "build"] 