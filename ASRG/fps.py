import time

def showFPS(times,start):
    end = time.time() - start
    times.append(end)
    if len(times) == 30:
        fps = sum(x for x in times)
        times.pop()
        print(f"{fps:.3f}")