BACKUP_DIR = .backup
CURRENT_DIR = .current

$(BACKUP_DIR):
	mkdir -p $(BACKUP_DIR)
	mkdir -p $(BACKUP_DIR)/.config

$(CURRENT_DIR):
	mkdir -p $(CURRENT_DIR)
	mkdir -p $(CURRENT_DIR)/.config

fonts:
	scripts/install_fonts.sh

install: $(fonts) $(BACKUP_DIR) $(CURRENT_DIR) $(CURRENT_CONFIG_DIR)
	scripts/install.py install

check:
	scripts/check_update.py

restore: $(BACKUP_DIR) $(CURRENT_DIR)
	scripts/install.py restore 
