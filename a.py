from camadaFisica import ErroMeioFisico

alist = [[0,1,1,0,1,1],[1,1,1,0,1,0,0]]

print(alist)

error = ErroMeioFisico(alist)
alist = error.erro()

print(alist)