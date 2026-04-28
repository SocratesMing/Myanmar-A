import uvicorn
import multiprocessing


def run_web():
    uvicorn.run("quant.app:app", host="0.0.0.0", port=8001, reload=True)


def run_api():
    uvicorn.run("quant.api:api_app", host="0.0.0.0", port=8002, reload=True)


def main():
    p1 = multiprocessing.Process(target=run_web)
    p2 = multiprocessing.Process(target=run_api)
    p1.start()
    p2.start()
    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()


if __name__ == "__main__":
    main()
