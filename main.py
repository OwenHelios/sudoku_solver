from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import Ui_MainWindow
import sys


def isValid(grid, i, j, x):
  for k in range(9):
    if grid[i][k] == x or grid[k][j] == x:
      return False
  st = i - i % 3
  sl = j - j % 3
  for a in range(st, st+3):
    for b in range(sl, sl+3):
      if grid[a][b] == x:
        return False
  return True


# class AlignDelegate(QtWidgets.QStyledItemDelegate):
#   def initStyleOption(self, option, index):
#     super(AlignDelegate, self).initStyleOption(option, index)
#     option.displayAlignment = QtCore.Qt.AlignCenter


class TableDelegate(QStyledItemDelegate):
  def __init__(self):
    super().__init__()

  def initStyleOption(self, option, index):
    super(TableDelegate, self).initStyleOption(option, index)
    option.displayAlignment = QtCore.Qt.AlignCenter

  def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
    super().paint(painter, option, index)

    painter.save()
    pen = QPen(QColor("black"))
    qr = QRect(option.rect)
    painter.setPen(pen)
    if index.row() % 3 == 2 and index.row() != 8:
      painter.drawLine(qr.bottomLeft(), qr.bottomRight())
    if index.column() % 3 == 2 and index.column() != 8:
      painter.drawLine(qr.topRight(), qr.bottomRight())
    painter.restore()


class Main(QMainWindow, Ui_MainWindow):

  def __init__(self: Ui_MainWindow, *args, **kwargs):
    QMainWindow.__init__(self, *args, **kwargs)
    self.setupUi(self)

    self.solution = list()
    self.capped = False
    self.tableWidget.setItemDelegate(TableDelegate())
    # delegate = AlignDelegate(self.tableWidget)
    # for i in range(9):
    #   self.tableWidget.setItemDelegateForColumn(i, delegate)

    self.btn_solve.clicked.connect(self.solve)
    self.btn_clear.clicked.connect(self.clear)

  def solve(self: Ui_MainWindow):
    grid = list([0]*9 for _ in range(9))
    for i in range(9):
      for j in range(9):
        item = self.tableWidget.item(i, j)
        if item and item.text().isdigit():
          grid[i][j] = int(item.text())
          # redBrush = QBrush(QColor(255, 0, 0))
          # item.setForeground(redBrush)

    self.dfs(grid, 0, 0)
    print(self.solution)

    # for i in range(9):
    #   for j in range(9):
    #     newItem = QTableWidgetItem(str(self.solution[i][j]))
    #     self.tableWidget.setItem(i, j, newItem)

    self.solution = []
    self.capped = False

  def dfs(self, grid, i, j):
    if self.capped:
      return
    while grid[i][j] != 0:
      if j < 8:
        j += 1
      elif i < 8 and j == 8:
        i += 1
        j = 0
      elif i == 8 and j == 8:
        self.solution.append([row[:] for row in grid])
        if len(self.solution) > 49:
          self.capped = True
        return
    for x in range(1, 10):
      if isValid(grid, i, j, x):
        grid[i][j] = x
        self.dfs(grid, i, j)
        grid[i][j] = 0

  # def dfs(self, grid, i, j):
  #   while grid[i][j] != 0:
  #     if j < 8:
  #       j += 1
  #     elif i < 8 and j == 8:
  #       i += 1
  #       j = 0
  #     elif i == 8 and j == 8:
  #       self.solution = grid
  #       return True
  #   for x in range(1, 10):
  #     if isValid(grid, i, j, x):
  #       grid[i][j] = x
  #       if self.dfs(grid, i, j):
  #         return True
  #       grid[i][j] = 0
  #   return False

  def clear(self: Ui_MainWindow):
    for i in range(9):
      for j in range(9):
        item = self.tableWidget.item(i, j)
        if item:
          item.setText("")
          darkBrush = QBrush(QColor(0, 0, 0))
          item.setForeground(darkBrush)

  def mouseReleaseEvent(self: Ui_MainWindow, QMouseEvent):
    if QMouseEvent.button() == Qt.LeftButton:
      self.tableWidget.clearSelection()


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = Main()
  MainWindow.show()
  sys.exit(app.exec_())

  # rowsMissing = list()
  # colsMissing = list()
  # squaresMissing = list()
  # cellsToFill = set()
  # poolForCell = dict()
  # solution = dict()

  # for i in range(9):
  #   full = set(range(1, 10))
  #   for j in range(9):
  #     if self.grid[i][j]:
  #       full.remove(i)
  #     else:
  #       cellsToFill.add((i, j))
  #   rowsMissing.append(full)

  # for col in list(zip(*self.grid)):
  #   full = set(range(1, 10))
  #   for i in col:
  #     if i:
  #       full.remove(i)
  #   colsMissing.append(full)

  # for i in range(9):
  #   full = set(range(1, 10))
  #   square = []
  #   x = (i//3)*3+1
  #   y = (i % 3)*3+1
  #   square += self.grid[x-1][y-1:y+2]
  #   square += self.grid[x][y-1:y+2]
  #   square += self.grid[x+1][y-1:y+2]
  #   for cell in square:
  #     if cell:
  #       full.remove(cell)
  #   squaresMissing.append(full)

  # for i, j in cellsToFill:
  #   squareIdx = j//3 + i - i % 3
  #   pool = set()
  #   for x in rowsMissing[i]:
  #     if x in colsMissing[j] and x in squaresMissing[squareIdx]:
  #       pool.add(x)
  #   if len(pool) == 1:
  #     solution[(i, j)] = next(iter(pool))
  #   else:
  #     poolForCell[(i, j)] = pool

  # if poolForCell:
  #   cells = poolForCell.keys()
  #   n = len(cells)
  #   for idx in range(n):
  #     pool = poolForCell[cells[idx]]
  #     while len(pool) > 1:
  #       tempPool = poolForCell.copy()
  #       x = next(iter(pool))

  # for (i, j), pool in poolForCell.items():
  #   tempPool = poolForCell.copy()
  #   while tempPool:
  #     i, j = next(iter(tempPool))
  #     while
