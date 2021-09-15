BACKUP_DIR = .backup
CURRENT_DIR = .current

$(BACKUP_DIR):
	mkdir -p $(BACKUP_DIR)

$(CURRENT_DIR):
	mkdir -p $(CURRENT_DIR)

system: $(BACKUP_DIR) $(CURRENT_DIR)
	python3 install.py apply $(CURRENT_DIR) $(BACKUP_DIR) system

i3: $(BACKUP_DIR) $(CURRENT_DIR)
	python3 install.py apply $(CURRENT_DIR) $(BACKUP_DIR) i3

reset: $(BACKUP_DIR) $(CURRENT_DIR)
	python3 install.py reset $(CURRENT_DIR) $(BACKUP_DIR) system i3
	
