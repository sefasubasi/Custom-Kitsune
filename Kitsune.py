import cupy as np
import time
from FeatureExtractor import FE
from KitNET.KitNET import KitNET
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

class Kitsune:
    def __init__(self, interface, limit, max_autoencoder_size=10, FM_grace_period=None, AD_grace_period=10000, learning_rate=0.1, hidden_ratio=0.75):
        self.FE = FE(interface, limit)
        self.AnomDetector = KitNET(self.FE.get_num_features(), max_autoencoder_size, FM_grace_period, AD_grace_period, learning_rate, hidden_ratio)

    def proc_next_packet(self):
        x = self.FE.get_next_vector()
        if len(x) == 0:
            return -1  # Error or no packets left
        return self.AnomDetector.process(x)  # Train during grace periods, then execute

if __name__ == "__main__":
    interface = "Wi-Fi"  # For Windows usually "Wi-Fi" or "Ethernet"
    packet_limit = np.Inf

    maxAE = 10
    FMgrace = 5000
    ADgrace = 50000

    K = Kitsune(interface, packet_limit, maxAE, FMgrace, ADgrace)

    print("Running Kitsune:")
    RMSEs = []
    i = 0
    start_time = time.time()
    max_duration = 5 * 60  # 5 minutes

    app = QApplication([])  # Correct use of QApplication
    win = pg.GraphicsLayoutWidget(title="Anomaly Scores from Kitsune's Execution Phase")  # Updated widget usage
    plot = win.addPlot(title="Real-Time RMSE Plot")
    curve = plot.plot(pen='y')

    timer = QTimer()

    def update():
        global RMSEs, curve, plot, i, start_time

        if i >= 75000:  # Stop after processing 75,000 packets
            timer.stop()
            app.quit()
            duration = time.time() - start_time
            print(f"Complete. Processed {i} packets. Time elapsed: {duration:.2f} seconds")
            return
        rmse = K.proc_next_packet()
        if rmse == -1:
            print("No more packets or error in processing.")
            timer.stop()
            app.quit()
            duration = time.time() - start_time
            print(f"Error encountered after {i} packets. Time elapsed: {duration:.2f} seconds")
            return
        RMSEs.append(rmse)
        if i % 1000 == 0 and i > 54000:  # Update the graph every 1000 packets
            curve.setData(RMSEs)
        i += 1

    timer.timeout.connect(update)
    timer.start(0)  # Immediately start the timer without delay

    win.show()  # Show window
    app.exec_()  # Start application
