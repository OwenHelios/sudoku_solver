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
    self.reset()
    self.tableWidget.setItemDelegate(TableDelegate())
    # delegate = AlignDelegate(self.tableWidget)
    # for i in range(9):
    #   self.tableWidget.setItemDelegateForColumn(i, delegate)

    self.btn_solve.clicked.connect(self.solve)
    self.btn_clear.clicked.connect(self.clear)
  
  def reset(self):
    self.grid = list([0]*9 for _ in range(9))
    self.rows = [0]*9
    self.cols = [0]*9
    self.blocks = [0]*9
    self.spaces = []

  def flip(self, i, j, bit):
    self.rows[i] ^= bit
    self.cols[j] ^= bit
    self.blocks[i // 3 * 3 + j // 3] ^= bit

  def solve(self: Ui_MainWindow):
    for i in range(9):
      for j in range(9):
        item = self.tableWidget.item(i, j)
        if item and item.text().isdigit():
          val = int(item.text()) - 1
          if val not in range(9):
            print(f"invalid value: ({i}, {j}) {item.text()}")
            return
          self.grid[i][j] = val
          self.flip(i, j, 1 << val)
          if (self.rows[i] & self.cols[j] & self.blocks[i // 3 * 3 + j // 3] & (1 << val)) == 0:
            print(f"invalid grid: ({i}, {j}) {item.text()}")
            return
          # redBrush = QBrush(QColor(255, 0, 0))
          # item.setForeground(redBrush)
        else:
          self.spaces.append((i, j))

    self.fill()

    for i in range(9):
      for j in range(9):
        newItem = QTableWidgetItem(str(self.grid[i][j] + 1))
        self.tableWidget.setItem(i, j, newItem)

  def fill(self):
    valid = False
    def dfs(pos):
      nonlocal valid
      if pos == len(self.spaces):
        valid = True
        return
      i, j = self.spaces[pos]
      mask = ~(self.rows[i] | self.cols[j] | self.blocks[i // 3 * 3 + j // 3]) & 0x1ff
      while mask:
        low_bit = mask & -mask
        self.flip(i, j, low_bit)
        self.grid[i][j] = len(bin(low_bit)) - 3
        dfs(pos + 1)
        if valid:
          return
        self.flip(i, j, low_bit)
        self.grid[i][j] = 0
        mask &= mask - 1
    dfs(0)

  def clear(self: Ui_MainWindow):
    self.reset()
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
