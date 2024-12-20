# Use a lightweight web server as the base
FROM nginx:stable-alpine

# Copy the React build files (from Vite) to the appropriate directory
COPY dist /usr/share/nginx/html

# Expose port 3000 for the frontend
EXPOSE 3000

# Run the Nginx server
CMD ["nginx", "-g", "daemon off;"]
