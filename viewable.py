import sqlite3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

np.set_printoptions(suppress=True)

con = sqlite3.connect('players.db')
cursorObj = con.cursor()
select_sql = 'select * from players'
results = cursorObj.execute(select_sql)

data = results.fetchall()
f = plt.figure(figsize=(100, 100), dpi=80)
ax = Axes3D(f)
ax.scatter(data[:, 3], data[:, 4], data[:, 5], c="b", label="3D")

plt.legend()
plt.show()
con.close()