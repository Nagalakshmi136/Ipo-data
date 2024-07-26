import hydra
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

from ipopy.data_fetchers.all_fetchers import fetch_ipo_data
from ipopy.notifications.email_notifier import EmailNotifier
from ipopy.notifications.notifier import Notifier
from ipopy.notifications.whatsapp_notifier import WhatsappNotifier


@hydra.main(
    config_path="ipopy/config", config_name="notifier_config", version_base=None
)
def main(cfg: DictConfig):
    config = OmegaConf.to_container(cfg, resolve=True)
    target_date = config.pop("target_date")
    notifier_config = config.pop("notifier")
    recipients = notifier_config.pop("recipients").split(" ")
    notifier_config["target_date"] = target_date
    print(notifier_config)
    ipo_data_with_sources = fetch_ipo_data(target_date)
    print(ipo_data_with_sources)
    notifier = Notifier.by_name(notifier_config.pop("type"))(**notifier_config)
    for recipient in tqdm(recipients):
        notifier.send_notification(recipient, ipo_data_with_sources)


if __name__ == "__main__":
    main()
