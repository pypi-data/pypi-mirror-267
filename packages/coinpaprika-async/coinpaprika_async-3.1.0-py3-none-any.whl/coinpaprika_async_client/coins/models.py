from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class CoinItem:
    id: str
    name: str
    symbol: str
    rank: int
    is_new: bool
    is_active: bool
    type: str


@dataclass
class Contract:
    contract: str
    platform: str
    type: str


@dataclass
class Links:
    explorer: List[str]
    facebook: List[str]
    reddit: List[str]
    source_code: List[str]
    website: List[str]
    youtube: List[str]
    medium: None


@dataclass
class Stats:
    subscribers: Optional[int]
    contributors: Optional[int]
    stars: Optional[int]


@dataclass
class LinksExtended:
    url: str
    type: str
    stats: Optional[Stats]


@dataclass
class Parent:
    id: str
    name: str
    symbol: str


@dataclass
class Tag:
    id: str
    name: str
    coin_counter: int
    ico_counter: int


@dataclass
class Team:
    id: str
    name: str
    position: str


@dataclass
class Whitepaper:
    link: str
    thumbnail: str


@dataclass
class Coin:
    id: str
    name: str
    symbol: str
    parent: Parent
    rank: int
    is_new: bool
    is_active: bool
    type: str
    logo: str
    tags: List[Tag]
    team: List[Team]
    description: str
    message: str
    open_source: bool
    hardware_wallet: bool
    started_at: datetime
    development_status: str
    proof_type: str
    org_structure: str
    hash_algorithm: str
    contract: str
    platform: str
    contracts: List[Contract]
    links: Links
    links_extended: List[LinksExtended]
    whitepaper: Whitepaper
    first_data_at: datetime
    last_data_at: datetime


@dataclass
class TwitterCoinItem:
    date: datetime
    user_name: str
    user_image_link: str
    status: str
    is_retweet: bool
    retweet_count: int
    like_count: int
    status_link: str
    status_id: str
    media_link: str
    youtube_link: str


@dataclass
class EventCoinItem:
    id: str
    date: datetime
    date_to: str
    name: str
    description: str
    is_conference: bool
    link: str
    proof_image_link: str


@dataclass
class Fiat:
    name: str
    symbol: str


@dataclass
class ExchangeCoinItem:
    id: str
    name: str
    fiats: List[Fiat]
    adjusted_volume_24h_share: float


@dataclass
class Key:
    price: float
    volume_24h: float


@dataclass
class MarketCoinItem:
    exchange_id: str
    exchange_name: str
    pair: str
    base_currency_id: str
    base_currency_name: str
    quote_currency_id: str
    quote_currency_name: str
    market_url: str
    category: str
    fee_type: str
    outlier: bool
    adjusted_volume_24h_share: float
    quotes: Dict[str, Key]
    last_updated: datetime


@dataclass
class CandleItem:
    time_open: datetime
    time_close: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    market_cap: int
