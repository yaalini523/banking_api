# Use official Node.js image (Alpine for smaller size)
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (exact versions from package-lock.json)
RUN npm ci

# Copy the rest of the app code
COPY . .

# Expose port 3000
EXPOSE 3000

# Default command: start the development server
CMD ["npm", "start"]
