"""
Tiny web app used to show how a Kubernetes Service load-balances across pods.

Each running pod answers with its own hostname. Because Kubernetes gives every
pod a unique hostname (the pod name), hitting the Service repeatedly and reading
the hostname back is a direct way to watch round-robin balancing in action.
"""
import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

# In a pod, Kubernetes sets HOSTNAME to the pod name, so this value differs per
# replica. socket.gethostname() is the fallback when running outside a pod.
POD_NAME = os.environ.get("HOSTNAME", socket.gethostname())


@app.route("/")
def index():
    # Returning the pod name is the whole point: the caller sees which replica
    # handled the request, which changes as the Service spreads load.
    return jsonify(message="hello from kubernetes", pod=POD_NAME)


@app.route("/healthz")
def healthz():
    # Liveness/readiness probes call this. Keeping it trivial (no DB, no deps)
    # means a pod is reported healthy only when the web server itself is up.
    return jsonify(status="ok", pod=POD_NAME)


if __name__ == "__main__":
    # 0.0.0.0 so the server is reachable from outside the container, not just
    # from localhost inside it. Port 8080 matches the containerPort in the manifest.
    app.run(host="0.0.0.0", port=8080)
