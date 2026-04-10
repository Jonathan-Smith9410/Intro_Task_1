# Stage 1: Test the config
FROM nginx:alpine as validate
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN nginx -t

# Stage 2: Final
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=validate /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/