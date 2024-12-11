# ClientDataManager
A Python microservice that validates incoming requests by checking if the source IP is within allowed AWS IP ranges for the Europe West region. It supports daily IP range updates and integrates with another microservice, forwarding unmodified HTTP headers for verification. Designed for enhanced security in Kubernetes environments.
