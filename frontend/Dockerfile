FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

EXPOSE 3000

ENV PORT 3000
# Starting locally in next start mode
CMD ["npm", "start"]