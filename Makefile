BACKUP_DIR = .backup
CURRENT_DIR = .current

$(BACKUP_DIR):
	mkdir -p $(BACKUP_DIR)
	mkdir -p $(BACKUP_DIR)/.config

$(CURRENT_DIR):
	mkdir -p $(CURRENT_DIR)
	mkdir -p $(CURRENT_DIR)/.config

install: $(BACKUP_DIR) $(CURRENT_DIR) $(CURRENT_CONFIG_DIR)
	scripts/install.py install

restore: $(BACKUP_DIR) $(CURRENT_DIR)
	scripts/install.py restore 
