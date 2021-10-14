BACKUP_DIR = .backup
CURRENT_DIR = .current

$(BACKUP_DIR):
	mkdir -p $(BACKUP_DIR)

$(CURRENT_DIR):
	mkdir -p $(CURRENT_DIR)

install: $(BACKUP_DIR) $(CURRENT_DIR)
	scripts/install.py install

restore: $(BACKUP_DIR) $(CURRENT_DIR)
	scripts/install.py restore 
