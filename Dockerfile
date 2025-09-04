FROM n8n/n8n:latest
COPY workflows/task_automation.json /root/.n8n/workflows/
COPY data/ /root/.n8n/data/
CMD ["n8n", "start"]