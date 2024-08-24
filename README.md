# Node-RED Qiskit functionality
To make quantum programming more accessible, we propose a learning and interactive platform based on Node-RED, integrated with Qiskit. Node-RED’s user-friendly visual interface simplifies the complexities of quantum programming by breaking down abstract concepts into manageable components. This approach bridges the gap between traditional programmers and those new to quantum computing, making the learning curve for Qiskit as intuitive as transitioning to object-oriented programming (OOP). This initiative aims to accelerate adoption and innovation in the quantum computing field.

Our goal is to abstract the core functionalities of the Qiskit library into Node-RED nodes, with each node representing a fundamental operation in quantum computing. This approach targets software developers with limited or no knowledge of quantum physics, helping them effectively utilize the Qiskit library.

To enhance learning, we have transformed the complex Qiskit documentation into easy-to-follow, graphical Node-RED flows. These flows break down content into clear, manageable steps with detailed explanations and code snippets, making quantum concepts more accessible. 
The designed nodes can be assembled into any quantum program. By interactively constructing complex quantum algorithms like the Quantum Approximate Optimization Algorithm (QAOA), we demonstrate how our flow programming framework promotes critical thinking about the sequence and structure of quantum programs. This hands-on approach allows users to experiment with different parameters and inputs, deepening their understanding of quantum computing.
## Prerequisites
- Node.js v21.0.0
- Node-RED v3.1.9
- Python3
## Installation
## How to Use
### Qiskit Learning flow
The Qiskit Learning Flow consists of a series of pre-built flows. To begin, you need to import the desired learning content from `./Learning/flows` into your Node-RED workspace and deploy it. Once deployed, you can follow these steps to explore and learn from the content in the flow:

1. Click the button on the _Start_ node to execute this flow.

2. Select the connected node and review the information in the sidebar. The information sidebar includes details on the quantum knowledge related to the node, code snippets, explanations of those code snippets, and information about Node input and output.
![image](https://github.com/Quantum-Node-RED/node-red-qiskit-functionality/blob/uniform-documentation-flow-style/Readme_Image/Learning_flow_step2.jpg)

3. After completing the current node, click on the _Next_ node and use the Information sidebar to learn about the connected node. Continue this process for each subsequent node.

4. After clicking the _Start_ or _Next_ node, if any connected nodes contain code snippets, these snippets will be executed. The results will either be displayed as images in the workspace or as text in the debug sidebar, helping users to better understand the code. (Tips: Some nodes require input parameters to execute their code. Please remember to open the _Edit palette_ to check if any parameters need to be entered)
![image](https://github.com/Quantum-Node-RED/node-red-qiskit-functionality/blob/uniform-documentation-flow-style/Readme_Image/Learning_flow_step4.jpg)

5. After you complete learning the content of a node, its status will change from red to green, indicating that you have studied the material in that node. This allows you to track your learning progress.
![image](https://github.com/Quantum-Node-RED/node-red-qiskit-functionality/blob/uniform-documentation-flow-style/Readme_Image/Learning_flow_step5.jpg)

6. Once completing your study, you can revisit the flow by re-importing and redeploying it for further learning.

## Contributing
## Acknowledgements
For more information about the authors, please refer to the [AUTHORS](./AUTHORS) file.

This Node-RED library was created as part of a partnership between [UCL IXN](https://www.ucl.ac.uk/computer-science/collaborate/ucl-industry-exchange-network-ucl-ixn) and [IBM](https://www.ibm.com/uk-en). IBM defined and arranged the project, which was assigned to students from UCL's Computer Science Department as part of their Master's thesis.  Special thanks go to John McNamara for managing the project's development, David Clark for serving as Academic Supervisors, and Roberto LoNardo for serving as our Quantum Mento advisors and guides.
