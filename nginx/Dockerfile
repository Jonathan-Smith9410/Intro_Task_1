# Stage 1: Validate
FROM nginx:alpine AS validate
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Comment out 'resolver' so 'nginx -t' doesn't try to ping the K8s DNS during build
RUN sed -i 's/resolver/#resolver/' /etc/nginx/conf.d/default.conf && nginx -t

# Stage 2: Final
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
# Copy the original config (with the resolver active)
COPY nginx.conf /etc/nginx/conf.d/default.conf