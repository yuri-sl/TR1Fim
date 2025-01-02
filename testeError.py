import matplotlib.pyplot as plt
import numpy as np

# Dados
x = np.linspace(0, 10, 100)
y = np.sin(x)
y_err = 0.2

# Gráfico com preenchimento de área de erro
plt.plot(x, y, label='Curva principal')
plt.fill_between(x, y - y_err, y + y_err, color='gray', alpha=0.3, label='Erro')
plt.title('Gráfico com área de erro')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
