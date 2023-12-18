import matplotlib.pyplot as plt
import numpy
from container import ContainerCircleSquare
import pandas

materials = ['Сталь_ХВГ', 'Полимерный_Композит_ПК_421', 'Латунь_113', 'Алюминиевый_Сплав_А231', 'Титановый_Сплав_Т12']

containers = []

for i in range(numpy.random.randint(3, 5)):
    containers.append(ContainerCircleSquare(
        material=numpy.random.choice(materials),
        emkost=numpy.random.uniform(95, 250),
        koeffC=numpy.random.uniform(0.15, 0.45)
    ))
    print(containers[i])

# 4 задание
for container in containers:
    container.optimizaciya()
    print(container)

# 5 задание
# сортировка по объёму
containers_by_emkost = sorted(containers, key=lambda container: container.emkost)

# сортировка по коэффициенту
containers_by_keofC = sorted(containers, key=lambda container: container.koeffC, reverse=True)

# сортировка по материалу
containers_by_material = sorted(containers, key=lambda container: container.material)

# сортировка по площади поверхности
containers_by_ff = sorted(containers, key=lambda container: container.F)

print('\nСписок сортированных резервуаров:')
print('По ёмкостям:\n', list(map(str, containers_by_emkost)))
print('По материалам:\n', list(map(str, containers_by_material)))
print('По коэффициенту C:\n', list(map(str, containers_by_keofC)))
print('По площади поверхности:\n', list(map(str, containers_by_ff)))

# 6 задание

V = numpy.random.uniform(95, 250)
container = ContainerCircleSquare(
    material=numpy.random.choice(materials),
    emkost=V,
    koeffC=numpy.random.uniform(0.15, 0.45)
)

plt.xlabel('Ряд шагов')
plt.ylabel('Ряд поверхностей')

for i in range(4):
    (spisok_shagov, spisok_poverhnostey) = container.optimizaciya()
    key = f"c = {container.koeffC}"

    df = pandas.DataFrame({
        'H': spisok_shagov,
        'F(H)': spisok_poverhnostey
    })
    df.to_excel(f'results/result_{i+1}_{key}.xlsx')
    df.to_csv(f'results/result_{i+1}_{key}.csv')
    df.to_csv(f'results/result_{i+1}_{key}.txt')

    plt.plot(spisok_shagov, spisok_poverhnostey, marker='o', label=key)
    container.koeffC = numpy.random.uniform(0.15, 0.45)

plt.legend()
plt.savefig('results/result.jpg')

plt.show()
