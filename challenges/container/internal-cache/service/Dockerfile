FROM redis:7.4-alpine
USER root
WORKDIR /app
COPY --chown=redis:redis redis.conf start.sh flag.txt /app/
RUN chmod 0555 /app/start.sh && chmod 0444 /app/redis.conf /app/flag.txt
USER redis
EXPOSE 6379
HEALTHCHECK --interval=15s --timeout=3s --start-period=15s --retries=3 CMD redis-cli PING | grep -q PONG
CMD ["sh", "/app/start.sh"]
