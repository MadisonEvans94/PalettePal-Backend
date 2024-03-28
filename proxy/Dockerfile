
# Use the official Nginx image
FROM nginx:alpine

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy a new configuration file
COPY nginx.conf /etc/nginx/conf.d/custom.conf