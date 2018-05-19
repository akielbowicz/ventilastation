from ventilagon import board

nave_pos = 360
#int nave_calibrate = -478 # ventilador velocidad media
nave_calibrate = -250 # ventilador velocidad maxima
half_ship_width = 50

volatile unsigned long last_turn = 0;
volatile unsigned long last_turn_duration = 10L;

void handle_interrupt() {
  unsigned long this_turn = micros();
  unsigned long this_turn_duration = this_turn - last_turn;
  //if (this_turn_duration < (last_turn_duration >> 2)) {
  //  return;
  //}
  last_turn_duration = this_turn_duration;
  last_turn = this_turn;
}

def reset():
    drift_pos = 0
    drift_speed = 0

drift_chance = 0

def adjust_drift():
    global drift_chance
    drift_chance = (drift_chance+1) & 0xF
    if drift_chance == 0:
        drift_speed = current_level.new_drift(drift_speed)


def ship_on(current_pos):
    if calibrating:
        return board.colision(current_pos, ROW_SHIP)

    # NO HAY QUE ARREGLAR NADA ACA
    if abs(nave_pos - current_pos) < half_ship_width:
        return true

    if abs(((nave_pos + SUBDEGREES / 2) & SUBDEGREES_MASK) -
           ((current_pos + SUBDEGREES / 2) & SUBDEGREES_MASK)
          ) < half_ship_width:
        return true

    return false


def tick(now):
    # esto no hace falta calcularlo tan seguido. Una vez por vuelta deberia alcanzar
    drift_pos = (drift_pos + drift_speed) & SUBDEGREES_MASK
    drift = drift_pos * last_turn_duration / SUBDEGREES
    current_pos = ((drift + now - last_turn) * SUBDEGREES / last_turn_duration) & SUBDEGREES_MASK
    current_column = ((drift + now - last_turn) * NUM_COLUMNS / last_turn_duration) % NUM_COLUMNS

    if ship_on(current_pos):
        ship.prender()
    else:
        ship.apagar()

    if current_column != last_column_drawn:
        board.draw_column(current_column)
