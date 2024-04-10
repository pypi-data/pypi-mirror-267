"""mget"""

import time
import asyncio
import logging
from typing import Callable, Any, Tuple, List, Optional, Coroutine, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from vxutils import logger

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def _http_get(url: str, *, parser: Callable[[httpx.Response], Any]) -> Any:
    async with httpx.AsyncClient() as client:
        for i in range(5):
            try:
                r = await client.get(url)
                r.raise_for_status()
                return parser(r)
            except httpx.HTTPError as e:
                logger.error("http error: %s", e)
                logger.info("第%s次重试...", i + 1)
                await asyncio.sleep(0.5)
        return await client.get(url)


class vxHttpGet:
    """多线程 http 链接"""

    __executor__ = ThreadPoolExecutor()

    def __init__(
        self,
        parser: Optional[Callable[[httpx.Response], Any]] = None,
        headers: Optional[httpx.Headers] = None,
        cookies: Optional[httpx.Cookies] = None,
        auth: Optional[Tuple[str, str]] = None,
        follow_redirects: Optional[bool] = None,
        timeout: float = 5,
        extensions: Optional[List] = None,
        retry_times: int = 5,
        workers: int = 10,
    ) -> None:
        self.parser = parser
        self.headers = headers
        self.cookies = cookies
        self.auth = auth
        self.flow_redirects = follow_redirects
        self.timeout = timeout
        self.extensions = extensions
        self.retry_times = retry_times
        self.workers = workers

    async def _task(
        self, method: Callable[[str], Coroutine[Any, Any, httpx.Response]], url: str
    ) -> str:
        for i in range(self.retry_times):
            try:
                r = await method(url)
                r.raise_for_status()
                if callable(self.parser):
                    return self.parser(r)
                return r.text
            except httpx.HTTPError as e:
                logger.error("http error: %s", e)
            except Exception as e:
                logger.error("parser error:%s, %s", r.text, e)
            logger.info("第%s次重试...", i + 1)
            await asyncio.sleep(0.5)
        return ""

    async def _get(self, *urls: str, **params: Any) -> List[str]:
        """执行连接"""

        async with httpx.AsyncClient(
            auth=self.auth,
            params=params,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
        ) as client:
            tasks = [self._task(client.get, url) for url in urls]
            return await asyncio.gather(*tasks)

    def __call__(self, *urls: str, **params: Any) -> List[str]:
        """mget"""
        if len(urls) == 1 and isinstance(urls[0], list):
            urls = urls[0]

        results = []
        for i in range(0, len(urls), self.workers):
            _urls = urls[i : i + self.workers]
            results.extend(
                self.__executor__.submit(
                    lambda: asyncio.run(self._get(*_urls, **params))
                ).result()
            )
            if i > 0:
                time.sleep(0.1)
        return results


class ThreadPoolMap:
    __executor__ = ThreadPoolExecutor()

    def __init__(self, func: Callable[[Any], Any], *iterable: Iterable[Any]) -> None:
        self.results = self.__executor__.map(func, iterable)

    def __iter__(self) -> Iterator[Any]:
        return self.results


if __name__ == "__main__":
    symbols = [
        "SH110043",
        "SH110044",
        "SH110045",
        "SH110047",
        "SH110048",
        "SH110052",
        "SH110053",
        "SH110055",
        "SH110057",
        "SH110058",
        "SH110059",
        "SH110060",
        "SH110061",
        "SH110062",
        "SH110063",
        "SH110064",
        "SH110067",
        "SH110068",
        "SH110070",
        "SH110072",
        "SH110073",
        "SH110074",
        "SH110075",
        "SH110076",
        "SH110077",
        "SH110079",
        "SH110080",
        "SH110081",
        "SH110082",
        "SH110083",
        "SH110084",
        "SH110085",
        "SH110086",
        "SH110087",
        "SH110088",
        "SH110089",
        "SH110090",
        "SH110091",
        "SH110092",
        "SH111000",
        "SH111001",
        "SH111002",
        "SH111003",
        "SH111004",
        "SH111005",
        "SH111006",
        "SH111007",
        "SH111008",
        "SH111009",
        "SH111010",
        "SH111011",
        "SH111012",
        "SH113011",
        "SH113013",
        "SH113016",
        "SH113017",
        "SH113021",
        "SH113024",
        "SH113025",
        "SH113027",
        "SH113030",
        "SH113033",
        "SH113037",
        "SH113039",
        "SH113042",
        "SH113043",
        "SH113044",
        "SH113045",
        "SH113046",
        "SH113047",
        "SH113048",
        "SH113049",
        "SH113050",
        "SH113051",
        "SH113052",
        "SH113053",
        "SH113054",
        "SH113055",
        "SH113056",
        "SH113057",
        "SH113058",
        "SH113059",
        "SH113060",
        "SH113061",
        "SH113062",
        "SH113063",
        "SH113064",
        "SH113065",
        "SH113504",
        "SH113505",
        "SH113516",
        "SH113519",
        "SH113524",
        "SH113526",
        "SH113527",
        "SH113530",
        "SH113532",
        "SH113534",
        "SH113535",
        "SH113537",
        "SH113542",
        "SH113545",
        "SH113546",
        "SH113549",
        "SH113561",
        "SH113563",
        "SH113565",
        "SH113566",
        "SH113567",
        "SH113569",
        "SH113570",
        "SH113573",
        "SH113574",
        "SH113575",
        "SH113576",
        "SH113577",
        "SH113578",
        "SH113579",
        "SH113582",
        "SH113584",
        "SH113585",
        "SH113588",
        "SH113589",
        "SH113591",
        "SH113593",
        "SH113594",
        "SH113595",
        "SH113596",
        "SH113597",
        "SH113598",
        "SH113600",
        "SH113601",
        "SH113602",
        "SH113604",
        "SH113605",
        "SH113606",
        "SH113608",
        "SH113609",
        "SH113610",
        "SH113615",
        "SH113616",
        "SH113618",
        "SH113619",
        "SH113621",
        "SH113622",
        "SH113623",
        "SH113624",
        "SH113625",
        "SH113626",
        "SH113627",
        "SH113628",
        "SH113629",
        "SH113631",
        "SH113632",
        "SH113633",
        "SH113634",
        "SH113636",
        "SH113637",
        "SH113638",
        "SH113639",
        "SH113640",
        "SH113641",
        "SH113643",
        "SH113644",
        "SH113646",
        "SH113647",
        "SH113648",
        "SH113649",
        "SH113650",
        "SH113651",
        "SH113652",
        "SH113653",
        "SH113654",
        "SH113655",
        "SH113656",
        "SH113657",
        "SH113658",
        "SH113659",
        "SH113660",
        "SH113661",
        "SH113662",
        "SH113663",
        "SH113664",
        "SH113665",
        "SH118000",
        "SH118003",
        "SH118004",
        "SH118005",
        "SH118006",
        "SH118007",
        "SH118008",
        "SH118009",
        "SH118010",
        "SH118011",
        "SH118012",
        "SH118013",
        "SH118014",
        "SH118015",
        "SH118016",
        "SH118017",
        "SH118018",
        "SH118019",
        "SH118020",
        "SH118021",
        "SH118022",
        "SH118023",
        "SH118024",
        "SH118025",
        "SH118026",
        "SH118027",
        "SH118028",
        "SH118029",
        "SH118030",
        "SZ123002",
        "SZ123004",
        "SZ123010",
        "SZ123011",
        "SZ123012",
        "SZ123013",
        "SZ123014",
        "SZ123015",
        "SZ123018",
        "SZ123022",
        "SZ123025",
        "SZ123031",
        "SZ123034",
        "SZ123035",
        "SZ123038",
        "SZ123039",
        "SZ123044",
        "SZ123046",
        "SZ123048",
        "SZ123049",
        "SZ123050",
        "SZ123052",
        "SZ123054",
        "SZ123056",
        "SZ123057",
        "SZ123059",
        "SZ123061",
        "SZ123063",
        "SZ123064",
        "SZ123065",
        "SZ123067",
        "SZ123071",
        "SZ123072",
        "SZ123075",
        "SZ123076",
        "SZ123077",
        "SZ123078",
        "SZ123080",
        "SZ123082",
        "SZ123083",
        "SZ123085",
        "SZ123087",
        "SZ123088",
        "SZ123089",
        "SZ123090",
        "SZ123091",
        "SZ123092",
        "SZ123093",
        "SZ123096",
        "SZ123098",
        "SZ123099",
        "SZ123100",
        "SZ123101",
        "SZ123103",
        "SZ123104",
        "SZ123105",
        "SZ123106",
        "SZ123107",
        "SZ123108",
        "SZ123109",
        "SZ123112",
        "SZ123113",
        "SZ123114",
        "SZ123115",
        "SZ123116",
        "SZ123117",
        "SZ123118",
        "SZ123119",
        "SZ123120",
        "SZ123121",
        "SZ123122",
        "SZ123124",
        "SZ123126",
        "SZ123127",
        "SZ123128",
        "SZ123129",
        "SZ123130",
        "SZ123131",
        "SZ123132",
        "SZ123133",
        "SZ123134",
        "SZ123135",
        "SZ123136",
        "SZ123138",
        "SZ123140",
        "SZ123141",
        "SZ123142",
        "SZ123143",
        "SZ123144",
        "SZ123145",
        "SZ123146",
        "SZ123147",
        "SZ123148",
        "SZ123149",
        "SZ123150",
        "SZ123151",
        "SZ123152",
        "SZ123153",
        "SZ123154",
        "SZ123155",
        "SZ123156",
        "SZ123157",
        "SZ123158",
        "SZ123159",
        "SZ123160",
        "SZ123161",
        "SZ123162",
        "SZ123163",
        "SZ123164",
        "SZ123165",
        "SZ123166",
        "SZ123167",
        "SZ123168",
        "SZ123169",
        "SZ123170",
        "SZ123171",
        "SZ123172",
        "SZ123173",
        "SZ127004",
        "SZ127005",
        "SZ127006",
        "SZ127007",
        "SZ127012",
        "SZ127014",
        "SZ127015",
        "SZ127016",
        "SZ127017",
        "SZ127018",
        "SZ127019",
        "SZ127020",
        "SZ127021",
        "SZ127022",
        "SZ127024",
        "SZ127025",
        "SZ127026",
        "SZ127027",
        "SZ127028",
        "SZ127029",
        "SZ127030",
        "SZ127031",
        "SZ127032",
        "SZ127033",
        "SZ127034",
        "SZ127035",
        "SZ127036",
        "SZ127037",
        "SZ127038",
        "SZ127039",
        "SZ127040",
        "SZ127041",
        "SZ127042",
        "SZ127043",
        "SZ127044",
        "SZ127045",
        "SZ127046",
        "SZ127047",
        "SZ127049",
        "SZ127050",
        "SZ127051",
        "SZ127052",
        "SZ127053",
        "SZ127054",
        "SZ127055",
        "SZ127056",
        "SZ127057",
        "SZ127058",
        "SZ127059",
        "SZ127060",
        "SZ127061",
        "SZ127062",
        "SZ127063",
        "SZ127064",
        "SZ127065",
        "SZ127066",
        "SZ127067",
        "SZ127068",
        "SZ127069",
        "SZ127070",
        "SZ127071",
        "SZ127072",
        "SZ127073",
        "SZ127074",
        "SZ127075",
        "SZ127076",
        "SZ127077",
        "SZ127078",
        "SZ127079",
        "SZ127080",
        "SZ128014",
        "SZ128017",
        "SZ128021",
        "SZ128023",
        "SZ128025",
        "SZ128026",
        "SZ128030",
        "SZ128033",
        "SZ128034",
        "SZ128035",
        "SZ128036",
        "SZ128037",
        "SZ128039",
        "SZ128040",
        "SZ128041",
        "SZ128042",
        "SZ128044",
        "SZ128048",
        "SZ128049",
        "SZ128053",
        "SZ128056",
        "SZ128062",
        "SZ128063",
        "SZ128066",
        "SZ128070",
        "SZ128071",
        "SZ128072",
        "SZ128074",
        "SZ128075",
        "SZ128076",
        "SZ128078",
        "SZ128079",
        "SZ128081",
        "SZ128082",
        "SZ128083",
        "SZ128085",
        "SZ128087",
        "SZ128090",
        "SZ128091",
        "SZ128095",
        "SZ128097",
        "SZ128100",
        "SZ128101",
        "SZ128105",
        "SZ128106",
        "SZ128108",
        "SZ128109",
        "SZ128111",
        "SZ128114",
        "SZ128116",
        "SZ128117",
        "SZ128118",
        "SZ128119",
        "SZ128120",
        "SZ128121",
        "SZ128122",
        "SZ128123",
        "SZ128124",
        "SZ128125",
        "SZ128127",
        "SZ128128",
        "SZ128129",
        "SZ128130",
        "SZ128131",
        "SZ128132",
        "SZ128133",
        "SZ128134",
        "SZ128135",
        "SZ128136",
        "SZ128137",
        "SZ128138",
        "SZ128140",
        "SZ128141",
        "SZ128142",
        "SZ128143",
        "SZ128144",
        "SZ128145",
    ]
    urls = [
        f"http://qt.gtimg.cn/q={','.join(symbols[i:i+80])}".lower()
        for i in range(0, len(symbols), 50)
    ]

    # print(urls)
    def http_get(url: str) -> List[str]:
        r = httpx.get(url)
        r.raise_for_status()
        return [line.split("~") for line in r.text.split("\n")]

    a = ThreadPoolMap(http_get, *urls)
    for i in a:
        print(i)
    raise SystemExit(0)

    def tencent_parser(response):
        """腾讯股票接口解析"""
        return [line.split("~") for line in response.text.split("\n")]

    hget = vxHttpGet(parser=tencent_parser, timeout=10)
    for r in hget(*urls):
        print(r[0])
        logger.info(len(r))
