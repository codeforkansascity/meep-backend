FROM nginx:1.15.12

# replace existing nginx.conf and default.conf files with our own config files
# last line of run makes directory for serving static files
RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx
