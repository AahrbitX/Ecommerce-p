# Step 1: Use Node.js for building the frontend
# Pull official Node.js image (use the LTS version)
FROM node:lts-slim

# Set working directory inside the container
WORKDIR /srv/app/

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . ./

# Expose the port for React app (usually port 3000 for development)
EXPOSE 3000

# Run the React development server
CMD ["npm", "start"]
