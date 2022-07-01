import mineField as mf

mine_field = mf.MineField(**mf.BEGINNER_FIELD)

print(mine_field.sweep_cell(5, 5))