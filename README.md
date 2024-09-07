# Kitsune
It is a network neural detection system that can detect online network attacks developed by Yisroel Mirsky and his team from Ben-Gurion University. KitNET, the core algorithm of Kitsune; It distinguishes normal and abnormal traffic patterns using an assembly of neural networks called autoencoders. Offering an innovative and effective solution in the field of network security, it can constantly monitor network traffic and detect anomalies providing protection against possible attacks. Thanks to these features, it is a flexible and powerful NIDS solution that can be used in different network environments.




# Kitsune Architecture
![An illustration of Kitsune's architecture](https://raw.githubusercontent.com/ymirsky/Kitsune-py/master/Kitsune_fig.png)
* External Libs: Kitsune depends on external libraries (libs) to capture and process network packets. These libraries provide packet capture and analysis functions. 
* Packet Capturer: Captures packets passing over the network. This module listens to network traffic and collects raw packet data required for further processing. 
* Packet Parser: Extracts necessary information from captured packets. This stage is critical for understanding the contents of the packets and converting them into usable data. 
* Feature Extractor (FE): Extracts features from data processed by the packet parser. Feature extraction ensures that data is made available for processing by the model. 
* Feature Mapper (FM): Converts the extracted features into a format that can be processed by autoencoders. This module ensures proper mapping and grouping of features. 
* Ensemble Layer: This is the layer where multiple autoencoders are located. Each autoencoder detects anomalies by working on certain feature groups. This layer consists of various autoencoders, each customized to detect different types of data anomalies. 
* Output Layer: It receives the information from the Ensemble layer and makes the final anomaly detection decision. This layer combines the outputs from all autoencoders to produce a final score or alarm. 
* ILog: Saves anomaly detection results. These logs are used to examine, report and archive detected events.




# Work Done 
Kitsune is a NIDS-based system that monitors malicious attacks (such as DOS, DDOS) in network traffic and produces RMSE values ​​​​based on these attacks. When we ran the system with the sample code we noticed that it was quite slow and cumbersome. To solve this problem we conducted research and focused on acceleration methods. We learned that parallel processing on graphics processors could speed up the system, and accordingly we started using the CUDA (cupy) library. As a result of these changes we observed that the system worked faster. Afterwards, we thought about how we can monitor anomalies that may occur in our own Wi-Fi network traffic with Kitsune and we deepened our research in this direction. We discovered that we could monitor network traffic using WireShark and process the resulting metrics in our program. We used the PyQt5 library to monitor the output of RMSE values ​​obtained from live traffic in the chart.

![kitsune](https://raw.githubusercontent.com/sefasubasi/Custom_Kitsune/main/resim.png)




Repository: https://github.com/ymirsky/Kitsune-py
