#include <iostream>
#include <vector>
#include <map>

class Asset {
public:
	std::string assetType;
	double balance;

	Asset(const std::string& type, double initialBalance)
		: assetType(type), balance(initialBalance) {}

	void transfer(double amount, const std::string& to) {
		// Симулация на трансфер на средства
		std::cout << "Transferring " << amount << " " << assetType << " to " << to << std::endl;
		balance -= amount;
	}
};

class Inheritor {
public:
	std::string name;
	std::string relationship;
	std::string contactInfo;

	Inheritor(const std::string& n, const std::string& rel, const std::string& contact)
		: name(n), relationship(rel), contactInfo(contact) {}

	void notify(double amount, const std::string& assetType) {
		std::cout << name << " has been notified of inheriting " << amount << " " << assetType << "." << std::endl;
	}
};

class User {
public:
	std::string username;
	std::string password;
	std::string email;
	std::vector<Asset> assets;
	std::vector<Inheritor> inheritors;

	User(const std::string& u, const std::string& p, const std::string& e)
		: username(u), password(p), email(e) {}

	void addAsset(const std::string& assetType, double initialBalance) {
		assets.emplace_back(assetType, initialBalance);
	}

	void transferAsset(double amount, const std::string& assetType, const std::string& to) {
		for (auto& asset : assets) {
			if (asset.assetType == assetType) {
				asset.transfer(amount, to);
				notifyInheritor(amount, assetType, to);
				return;
			}
		}
		std::cerr << "Asset type not found: " << assetType << std::endl;
	}

	void addInheritor(const std::string& name, const std::string& relationship, const std::string& contactInfo) {
		inheritors.emplace_back(name, relationship, contactInfo);
	}

	void removeInheritor(const std::string& name) {
		inheritors.erase(std::remove_if(inheritors.begin(), inheritors.end(),
			[name](const Inheritor& inheritor) { return inheritor.name == name; }),
			inheritors.end());
	}

private:
	void notifyInheritor(double amount, const std::string& assetType, const std::string& to) {
		for (const auto& inheritor : inheritors) {
			if (inheritor.relationship == "Inherits" && inheritor.contactInfo == to) {
				inheritor.notify(amount, assetType);
				return;
			}
		}
	}
};

int main() {
	User user("JohnDoe", "password123", "john.doe@email.com");
	user.addAsset("Bitcoin", 5.0);
	user.addAsset("Ethereum", 10.0);
	user.addInheritor("Alice", "Inherits", "Alice's contact");

	user.transferAsset(3.0, "Bitcoin", "Alice");

	user.removeInheritor("Alice"); // Пример за изтриване на наследник

	return 0;
}