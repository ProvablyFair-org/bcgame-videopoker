// Compare BC's public bet records with this package. Paste into the browser console on https://bc.game and wait about a minute.
// Written by checks/make_bc_compare.py from the bet records in evidence/. No login needed; nothing is sent anywhere else.
// Each bet: SHA-256 fingerprints of six field groups (game, bet, seeds, selection, cards, money); see make_bc_compare.py.
(async () => {
  const GROUPS = ["game", "bet", "seeds", "selection", "cards", "money"];
  const expected = {
 "1882023973566199191": [
  "dd05278d5c47c299",
  "c1e1e8c2f194e4b4",
  "6f7725fd14383fbf",
  "3d3bc3d06f185da3",
  "b619e76c67a96de2",
  "24aeb9974b784660"
 ],
 "1882023978475633016": [
  "dd05278d5c47c299",
  "a79f64c5d1d52260",
  "5eccdf10b738b870",
  "1c64ae1fe067a8f7",
  "02d074dcfa54d6d2",
  "24aeb9974b784660"
 ],
 "1882023983546543889": [
  "dd05278d5c47c299",
  "c3b06009505be045",
  "e88ab40805b195ea",
  "8b27ea8edcd45264",
  "c00c5c522b919f4a",
  "24aeb9974b784660"
 ],
 "1882024254455591507": [
  "dd05278d5c47c299",
  "993f29cb70631ecf",
  "668fb6baef43100c",
  "21a623bb47ad97bf",
  "000d870cac5d5e89",
  "24aeb9974b784660"
 ],
 "1882024259533845990": [
  "dd05278d5c47c299",
  "9748645e14aca5b0",
  "47c84d6eaf9b9aee",
  "fd3b20e6578c3db2",
  "ef4d89c0ff8d1f24",
  "24aeb9974b784660"
 ],
 "1882024264473684728": [
  "dd05278d5c47c299",
  "8ecacefb777031c0",
  "fae20543b3936d26",
  "da115a806e38d839",
  "f04e8420e39e76cf",
  "24aeb9974b784660"
 ],
 "1882024269419818575": [
  "dd05278d5c47c299",
  "4b0f212ceeafa6ce",
  "1f17d0c20492bdc9",
  "d5a8c4dcf8290360",
  "4f22a81f1d9f358d",
  "24aeb9974b784660"
 ],
 "1882024274367000910": [
  "dd05278d5c47c299",
  "33cb56f9590ef95f",
  "59fe20d2f9ff203a",
  "5651c93362d63852",
  "e033b150f359a69a",
  "24aeb9974b784660"
 ],
 "1882024279355084248": [
  "dd05278d5c47c299",
  "47e1bd7452e5869b",
  "02800ecb4df4f7b1",
  "a4fcc2a8efa3d799",
  "d7be47a02023221e",
  "24aeb9974b784660"
 ],
 "1882024287033803500": [
  "dd05278d5c47c299",
  "56bbce532f48e276",
  "9412ac6b2f72a12b",
  "725af60e0fb9dbb4",
  "6c0ae2604561b342",
  "471fb79d127e60cf"
 ],
 "1882024289360591748": [
  "dd05278d5c47c299",
  "e848a896ae4834d9",
  "cae398b6ae2f4a8c",
  "4eb660fce4fbbb18",
  "d1cfea807b6dec3f",
  "24aeb9974b784660"
 ],
 "1882024294279455156": [
  "dd05278d5c47c299",
  "027595c2da9a1ada",
  "d0f246625f21affc",
  "4f4dfddde6767b51",
  "7278c0004fa48fb5",
  "24aeb9974b784660"
 ],
 "1882024299353515313": [
  "dd05278d5c47c299",
  "b6b59bc3c3fe1cff",
  "c7d15a796d6e9edd",
  "4b668c497cbf21b5",
  "fc1cb5acd425b268",
  "24aeb9974b784660"
 ],
 "1882024304273434789": [
  "dd05278d5c47c299",
  "503c257029477acf",
  "9169e41c89c5840c",
  "62ea768fdcbd0b5b",
  "dccae25983929bb2",
  "24aeb9974b784660"
 ],
 "1882024309188117056": [
  "dd05278d5c47c299",
  "a0247fda883a7e44",
  "2cbd79c6b09ea692",
  "d761081a7e0a8746",
  "1e48f0c2dc73db4b",
  "24aeb9974b784660"
 ],
 "1882024314133200150": [
  "dd05278d5c47c299",
  "607e3e9a856b4932",
  "03c623f1def0c3cc",
  "0ccafad55a7f9b56",
  "312192aeb453bdf9",
  "24aeb9974b784660"
 ],
 "1882024319058358851": [
  "dd05278d5c47c299",
  "29aaddfe7f9707f0",
  "a73197a7e62a9982",
  "cf4d4be06a9fe26a",
  "6923e1c9a709e9d2",
  "24aeb9974b784660"
 ],
 "1882024323980372107": [
  "dd05278d5c47c299",
  "28df695270001837",
  "6b66967fb4188421",
  "237305c6318837f6",
  "37c40989b75ca3dc",
  "24aeb9974b784660"
 ],
 "1882024328905540066": [
  "dd05278d5c47c299",
  "40b15343833d8293",
  "afb092dca5019a2c",
  "72aa2d2ec2ba816a",
  "f145d7a6e5ec9401",
  "24aeb9974b784660"
 ],
 "1882024664905985714": [
  "dd05278d5c47c299",
  "061e0ecf29b06df3",
  "89d472f49d4c3b68",
  "0edc6990d6fa20f8",
  "d128ad900ce36b98",
  "24aeb9974b784660"
 ],
 "1882024672480899502": [
  "dd05278d5c47c299",
  "da046bcd40ee0471",
  "bffc9e48a92a40e2",
  "36e4cd78feb04b6c",
  "811d9cb2ffe2b44a",
  "a952b3aa18839f6c"
 ],
 "1882024675020551006": [
  "dd05278d5c47c299",
  "5f1e0c002bff0ab2",
  "889a9c92752bee04",
  "606930ebcc4689de",
  "7de4e1ad269e327f",
  "24aeb9974b784660"
 ],
 "1882024683296959446": [
  "dd05278d5c47c299",
  "78bf6cc8d5170c05",
  "d0a802a43d41cf54",
  "4667251fb05f2fed",
  "ddcbb74f3d26c4b4",
  "70af0a6d22cc1744"
 ],
 "1882024688748507048": [
  "dd05278d5c47c299",
  "5d8921d837bcc50b",
  "4fd9f7b150e3d2e3",
  "f6b928c9f0af8894",
  "629a34794d35581a",
  "a952b3aa18839f6c"
 ],
 "1882024690457682141": [
  "dd05278d5c47c299",
  "814ce3186af34755",
  "eaaf4828f94e5c59",
  "1a3a298b58cdf51b",
  "48917c83388ac0dc",
  "24aeb9974b784660"
 ],
 "1882024695496100579": [
  "dd05278d5c47c299",
  "aa7085b822505d65",
  "f3b01b1b941031f8",
  "ceb5564592ee6b99",
  "1d52cf22f5f1b74f",
  "24aeb9974b784660"
 ],
 "1882024700439088759": [
  "dd05278d5c47c299",
  "10acaec7e4cacc40",
  "e387e50c507add02",
  "3374b2ce40507a52",
  "406dc76218f3a609",
  "24aeb9974b784660"
 ],
 "1882024708707102704": [
  "dd05278d5c47c299",
  "460d49e8108d36f5",
  "e068d3780ca4c000",
  "22711ff8dcdfa90b",
  "04035c572c6aa7f5",
  "70af0a6d22cc1744"
 ],
 "1882024710553641282": [
  "dd05278d5c47c299",
  "47d92cc26a3d8d2c",
  "d89f83ef35ca4bd4",
  "cce0e00d4381bbae",
  "48cd6a539c2e0ee8",
  "24aeb9974b784660"
 ],
 "1882024715639235732": [
  "dd05278d5c47c299",
  "dbb56d9fdff6969d",
  "5869ad0e9dae0875",
  "55dd90efd11e911b",
  "b65b2e5be58707ae",
  "24aeb9974b784660"
 ],
 "1882024720782511949": [
  "dd05278d5c47c299",
  "bc80b942beadeda8",
  "d7f716632e5f8e3d",
  "be3017b41056b907",
  "bb86cfac6148e555",
  "24aeb9974b784660"
 ],
 "1882024725852373818": [
  "dd05278d5c47c299",
  "f5bf02022d530264",
  "aa6a4693d633ca2d",
  "72e16b7b082959ee",
  "f7a39d3184e89ca6",
  "24aeb9974b784660"
 ],
 "1882025640373169122": [
  "dd05278d5c47c299",
  "39f5af333bf33526",
  "b70476b04b77d3ea",
  "f3c930da8b750575",
  "16834c7d975baeef",
  "24aeb9974b784660"
 ],
 "1882025645534261157": [
  "dd05278d5c47c299",
  "b2d6f4cf42c0ede6",
  "1a2b3f5b354e0070",
  "f0c2a4b81299a445",
  "45b1e9926b88a365",
  "24aeb9974b784660"
 ],
 "1882025649311228486": [
  "dd05278d5c47c299",
  "c8dc4f1b988721eb",
  "13ea81f54b7aabd3",
  "553aabc052a8b445",
  "712e2394ae0398f9",
  "24aeb9974b784660"
 ],
 "1882025653706863917": [
  "dd05278d5c47c299",
  "000caeae2a66d28e",
  "fb2f9661899c2c03",
  "1abb1b40c17412b2",
  "409e06b811aa7f1f",
  "24aeb9974b784660"
 ],
 "1882025657581349556": [
  "dd05278d5c47c299",
  "a94e0db22afc343f",
  "a8fec69218f1d68d",
  "788743e389cfb64a",
  "d51cdb8c8a8a21ec",
  "24aeb9974b784660"
 ],
 "1882025661947625811": [
  "dd05278d5c47c299",
  "15add1b15bd63490",
  "07328d17db003913",
  "e5263da431ef4195",
  "fe776d4e1038e65d",
  "24aeb9974b784660"
 ],
 "1882025668360708643": [
  "dd05278d5c47c299",
  "4fbbc51510763623",
  "e5311e6aa961abc8",
  "7e4f1ce95c9caa1c",
  "98a32d383c7eaaba",
  "70af0a6d22cc1744"
 ],
 "1882025670544896640": [
  "dd05278d5c47c299",
  "3acf2c7b3f5b0577",
  "1d444a7924f8bdc4",
  "478c793614a25749",
  "182cab220afcc44b",
  "24aeb9974b784660"
 ],
 "1882025674854541090": [
  "dd05278d5c47c299",
  "7ccde5f4d15c2c37",
  "d0e574093482da14",
  "efde6ff39d2593d6",
  "ef077be7dfe1bb69",
  "24aeb9974b784660"
 ],
 "1882025681204722240": [
  "dd05278d5c47c299",
  "91351df9fcd008ee",
  "6ec7c169c3cd07f1",
  "4d060ceb1bd5582c",
  "3ca2828e5aab5695",
  "22f6d97fdd41da2d"
 ],
 "1882025684499348674": [
  "dd05278d5c47c299",
  "dc177a056e438275",
  "18893dd5a1f1b1f7",
  "eda892213c955e68",
  "334bed6e7369d307",
  "b0bcc62f1d689a18"
 ],
 "1882025686829286514": [
  "dd05278d5c47c299",
  "e59a3c99fd76c90c",
  "be316ab819f283cd",
  "697f93a8806b7132",
  "febcd16ce78749d7",
  "24aeb9974b784660"
 ],
 "1882025691196606696": [
  "dd05278d5c47c299",
  "23b9831cd865af37",
  "913448293a198d71",
  "7eea68a486c5cdfb",
  "e838327dd13b2f5a",
  "24aeb9974b784660"
 ],
 "1882025696936512691": [
  "dd05278d5c47c299",
  "11967dfd732a243d",
  "b31a1f3b0fb12ce3",
  "a36232ffded498f6",
  "0f491ffd8fc46e96",
  "a952b3aa18839f6c"
 ],
 "1882025701008125252": [
  "dd05278d5c47c299",
  "08d8aaf9da8fd026",
  "2f18aa23064ad90d",
  "24aba410d679b470",
  "f8dcd275f389b073",
  "b0bcc62f1d689a18"
 ],
 "1882025705390121348": [
  "dd05278d5c47c299",
  "bb191f51442b28d2",
  "e5771be04c65d10f",
  "0dbb4e36615c258d",
  "fda1afc8bf5c7d62",
  "a952b3aa18839f6c"
 ],
 "1882025709671457886": [
  "dd05278d5c47c299",
  "111473c0b65ac054",
  "264dc337be7bf44f",
  "ce7414d806b7dfe8",
  "67f582355e9986aa",
  "a952b3aa18839f6c"
 ],
 "1882025713900365640": [
  "dd05278d5c47c299",
  "45e9a22515bd2dd1",
  "8ca3b10e46276193",
  "9385c79bb7b01e66",
  "04f0a9ea7a7c68e9",
  "70af0a6d22cc1744"
 ],
 "1882025715977595068": [
  "dd05278d5c47c299",
  "d727290055a30882",
  "458a1e4cdd2a8dc2",
  "d0f67a8306274158",
  "7f926d15ad88c507",
  "24aeb9974b784660"
 ],
 "1882025722338263306": [
  "dd05278d5c47c299",
  "3aff8addbc91bc22",
  "8126f6d403f0d87e",
  "9406bf04d47b62ef",
  "5cb3f0f1064f6947",
  "70af0a6d22cc1744"
 ],
 "1882025724708045572": [
  "dd05278d5c47c299",
  "2cb49b57fd86f677",
  "97359220a9b8b0f7",
  "abeb161216406e85",
  "6ff56c39ffae7d4e",
  "24aeb9974b784660"
 ],
 "1882025729368967097": [
  "dd05278d5c47c299",
  "8bb213a1199841aa",
  "a886ab1e90479ef7",
  "25acc676696b71ad",
  "4982900edaf9a6e7",
  "24aeb9974b784660"
 ],
 "1882025735733819267": [
  "dd05278d5c47c299",
  "cee4407decc7648c",
  "cdbd0b19392bef0c",
  "58890c987ce88e0c",
  "fb9a13b810940645",
  "70af0a6d22cc1744"
 ],
 "1882025740095892502": [
  "dd05278d5c47c299",
  "5b43fd98ec0d780a",
  "f4104c6ff40676e9",
  "78ca479a917b1186",
  "45d34a20a9e48bd4",
  "a952b3aa18839f6c"
 ],
 "1882025742781300942": [
  "dd05278d5c47c299",
  "2bf7df93d2cacec2",
  "7d13d6914375c038",
  "414eb0dba28c691c",
  "0673d0e0a924503f",
  "24aeb9974b784660"
 ],
 "1882025747172738079": [
  "dd05278d5c47c299",
  "0977478da3f533d1",
  "7d34afb397ed9662",
  "731b41353ffec382",
  "55b79f5df6897145",
  "24aeb9974b784660"
 ],
 "1882025753572193194": [
  "dd05278d5c47c299",
  "a92c193685e3bd98",
  "e35ceacd59c254fd",
  "b5f8c2e4ced3b090",
  "c4188fa16cc78289",
  "70af0a6d22cc1744"
 ],
 "1882025755568687587": [
  "dd05278d5c47c299",
  "98c5c15210f8b5f3",
  "0734359b4fd216d3",
  "07a555ab5d37c2ca",
  "c4d9190cff7c4b87",
  "24aeb9974b784660"
 ],
 "1882025759942299296": [
  "dd05278d5c47c299",
  "3c98cd9fc0305ab5",
  "26e465b5ff596af2",
  "58890c987ce88e0c",
  "2412f7812d2ff23f",
  "24aeb9974b784660"
 ],
 "1882025764319052290": [
  "dd05278d5c47c299",
  "fba898d4e8427168",
  "00383c38084b9f84",
  "14c6f3dfccc20c30",
  "72afa9b860bbb6d1",
  "24aeb9974b784660"
 ],
 "1882030457102450980": [
  "eebc9ffbbfcc9f20",
  "0e09c483bf297f8c",
  "7f14c51b3a8bc993",
  "7793faeecfea4d6b",
  "79dbcdba666b6435",
  "bbcd0238701a15f6"
 ],
 "1882030461885001818": [
  "eebc9ffbbfcc9f20",
  "14d28337b93f4516",
  "15de5b67e1f77716",
  "7793faeecfea4d6b",
  "ee9e6517222ba9f4",
  "bbcd0238701a15f6"
 ],
 "1882030466123352501": [
  "eebc9ffbbfcc9f20",
  "7d2204cc451c8d95",
  "f4622449072b95ff",
  "7793faeecfea4d6b",
  "9308a82b2598ba58",
  "98c3fe1beda6569e"
 ],
 "1882030471406073663": [
  "eebc9ffbbfcc9f20",
  "0a32a469191a15f2",
  "dc25f551b1e7ec68",
  "7793faeecfea4d6b",
  "d8c8bf327276cb0e",
  "98c3fe1beda6569e"
 ],
 "1882030476512639769": [
  "eebc9ffbbfcc9f20",
  "46171ee1dcd5f9ea",
  "759ac970434ddc65",
  "7793faeecfea4d6b",
  "a55a134b73a326c5",
  "984b7311e8ab77bc"
 ],
 "1882030480776143351": [
  "eebc9ffbbfcc9f20",
  "c1c0ff5c6bb29a19",
  "60a6b8d38b0dece0",
  "7793faeecfea4d6b",
  "30a3e878a4c548f4",
  "bbcd0238701a15f6"
 ],
 "1882030485577583373": [
  "eebc9ffbbfcc9f20",
  "7b706376cc4c7e0d",
  "2dc9adf311f6e4f1",
  "7793faeecfea4d6b",
  "7309330ee6fd45e7",
  "bbcd0238701a15f6"
 ],
 "1882030489809627550": [
  "eebc9ffbbfcc9f20",
  "54817c0585cef72e",
  "379ee2cfe97ef202",
  "7793faeecfea4d6b",
  "15ad6cc01116cf9d",
  "98c3fe1beda6569e"
 ],
 "1882030495196168739": [
  "eebc9ffbbfcc9f20",
  "e7f8cbcc6fd2fd57",
  "de7a70b6c12670c8",
  "7793faeecfea4d6b",
  "7422c373d5d9fcd5",
  "bbcd0238701a15f6"
 ],
 "1882030499459678069": [
  "eebc9ffbbfcc9f20",
  "bd3c2bf6b728c2ab",
  "3bdfcc1e8f3e5175",
  "7793faeecfea4d6b",
  "e98f4d6ceec0b193",
  "bbcd0238701a15f6"
 ],
 "1882030503742059415": [
  "eebc9ffbbfcc9f20",
  "f540cc061697be7f",
  "2475d996683f6123",
  "7793faeecfea4d6b",
  "f3a12abcd856bac1",
  "bbcd0238701a15f6"
 ],
 "1882030509047861105": [
  "eebc9ffbbfcc9f20",
  "987a4c55e6a383a1",
  "e826ff89041b7924",
  "7793faeecfea4d6b",
  "2070e96d49d9456e",
  "bbcd0238701a15f6"
 ],
 "1882030514442776291": [
  "eebc9ffbbfcc9f20",
  "65b4501f2c1730c5",
  "ed751a957ff90c44",
  "7793faeecfea4d6b",
  "17cf4d65c18b4afb",
  "98c3fe1beda6569e"
 ],
 "1882030518706282955": [
  "eebc9ffbbfcc9f20",
  "fb9581265281c8ec",
  "6c6d7d1eb3379535",
  "7793faeecfea4d6b",
  "ed301e55c84baf15",
  "984b7311e8ab77bc"
 ],
 "1882030522941491883": [
  "eebc9ffbbfcc9f20",
  "e438893aad716f49",
  "43b8bb7aae785131",
  "7793faeecfea4d6b",
  "90d5817c532c9f42",
  "98c3fe1beda6569e"
 ],
 "1882030527735576775": [
  "eebc9ffbbfcc9f20",
  "7b2cb0bf1e88be4e",
  "cba010c4d792325e",
  "7793faeecfea4d6b",
  "b5524be3a2d50208",
  "984b7311e8ab77bc"
 ],
 "1882030533143080641": [
  "eebc9ffbbfcc9f20",
  "52717be8f5802af8",
  "a6c89c44db13746e",
  "7793faeecfea4d6b",
  "b38e25b33d11dbbd",
  "bbcd0238701a15f6"
 ],
 "1882030538439444196": [
  "eebc9ffbbfcc9f20",
  "b999967c027ed3c1",
  "850366149c0506cc",
  "7793faeecfea4d6b",
  "2f32f9ddc5062551",
  "bbcd0238701a15f6"
 ],
 "1882030542696663742": [
  "eebc9ffbbfcc9f20",
  "653f262719f26876",
  "31d9f40b2ddbef2e",
  "7793faeecfea4d6b",
  "8e3f6788903480d0",
  "250638b67063bf5c"
 ],
 "1882030547985682129": [
  "eebc9ffbbfcc9f20",
  "9e725a17bc5be453",
  "44cd1c4d80afbe40",
  "7793faeecfea4d6b",
  "ee985c359b3e23d3",
  "bbcd0238701a15f6"
 ],
 "1882030552226120154": [
  "eebc9ffbbfcc9f20",
  "a9e503fa59f9aa29",
  "fb24513798193819",
  "7793faeecfea4d6b",
  "08d353a1cfaeab24",
  "98c3fe1beda6569e"
 ],
 "1882030556469707995": [
  "eebc9ffbbfcc9f20",
  "f40f22ba2afe4a8d",
  "2b0a89c616a616b6",
  "7793faeecfea4d6b",
  "423eb3fb5af470f5",
  "bbcd0238701a15f6"
 ],
 "1882030560699664306": [
  "eebc9ffbbfcc9f20",
  "e2c522d13f550de9",
  "391400251eb09992",
  "7793faeecfea4d6b",
  "ee1bc91a27012ed7",
  "984b7311e8ab77bc"
 ],
 "1882030565573437386": [
  "eebc9ffbbfcc9f20",
  "b7794825e040be39",
  "a982661faf655239",
  "7793faeecfea4d6b",
  "046dcb90aff2e755",
  "98c3fe1beda6569e"
 ],
 "1882030571063787880": [
  "eebc9ffbbfcc9f20",
  "fbe32bf7da7c92cb",
  "9fba07d423ceb69a",
  "7793faeecfea4d6b",
  "e95cf7cf828ee70e",
  "bbcd0238701a15f6"
 ],
 "1882030576386358867": [
  "eebc9ffbbfcc9f20",
  "22deb74a24aa767d",
  "3e1479b1fd292b08",
  "7793faeecfea4d6b",
  "a2820c3441dffee1",
  "984b7311e8ab77bc"
 ],
 "1882030580648822734": [
  "eebc9ffbbfcc9f20",
  "7c41aeca2a55262a",
  "326f39802707e85d",
  "7793faeecfea4d6b",
  "0d35cfba38ebb831",
  "bbcd0238701a15f6"
 ],
 "1882030584864089697": [
  "eebc9ffbbfcc9f20",
  "49065b7570c92242",
  "bc3f29b9bf19b4e8",
  "7793faeecfea4d6b",
  "3606c116c962aa76",
  "bbcd0238701a15f6"
 ],
 "1882030590311443646": [
  "eebc9ffbbfcc9f20",
  "8b05d403a4cc004d",
  "9577b3eedae075b3",
  "7793faeecfea4d6b",
  "a4220b84d72bb1e2",
  "bbcd0238701a15f6"
 ],
 "1882030594557133967": [
  "eebc9ffbbfcc9f20",
  "544cddc41915290c",
  "b649ad027a0cbbe4",
  "7793faeecfea4d6b",
  "9d6d11285b1b0ac1",
  "98c3fe1beda6569e"
 ],
 "1882030599318718410": [
  "eebc9ffbbfcc9f20",
  "fc3d906b151228ec",
  "e35ae6c4eb17e810",
  "7793faeecfea4d6b",
  "6537229cfe087517",
  "bbcd0238701a15f6"
 ],
 "1882030604619265224": [
  "eebc9ffbbfcc9f20",
  "1c5837ee801efadf",
  "229f5e4014ba9f5a",
  "7793faeecfea4d6b",
  "992c53a38b4c8211",
  "98c3fe1beda6569e"
 ],
 "1882030609378754748": [
  "eebc9ffbbfcc9f20",
  "b8e7781bfa5ef6ce",
  "5788d471f1e2ecff",
  "7793faeecfea4d6b",
  "cdf4be41d5746589",
  "0052b71e849469e6"
 ],
 "1882030613607662739": [
  "eebc9ffbbfcc9f20",
  "fbeab6f7ba6d045f",
  "c9217168294b1365",
  "7793faeecfea4d6b",
  "5dab0d97e0d84614",
  "98c3fe1beda6569e"
 ],
 "1882030618372383522": [
  "eebc9ffbbfcc9f20",
  "a6b2b89e91fd5fc2",
  "0cc2b5a12615cd1d",
  "7793faeecfea4d6b",
  "45f3da7ffa1506f6",
  "250638b67063bf5c"
 ],
 "1882030622614926280": [
  "eebc9ffbbfcc9f20",
  "5a0e249b9ba0929d",
  "3b7beff57e4317dd",
  "7793faeecfea4d6b",
  "f48d372018018adc",
  "bbcd0238701a15f6"
 ],
 "1882030626876336858": [
  "eebc9ffbbfcc9f20",
  "8d63c452567ecb4c",
  "cdb07c2045e57fbf",
  "7793faeecfea4d6b",
  "18f3bac29749c56c",
  "98c3fe1beda6569e"
 ],
 "1882030631135658838": [
  "eebc9ffbbfcc9f20",
  "858c860949cf598f",
  "0a23fd289d53c2d6",
  "7793faeecfea4d6b",
  "c3de5c608a8f13a1",
  "bbcd0238701a15f6"
 ],
 "1882030788412624543": [
  "eebc9ffbbfcc9f20",
  "230724e7e5bb4a34",
  "48a2f96f221d69bc",
  "71a6bab591e66e95",
  "cbf24be46297dbc5",
  "98c3fe1beda6569e"
 ],
 "1882030793753014240": [
  "eebc9ffbbfcc9f20",
  "6902d17fbf599199",
  "cce3b8de1745eb6b",
  "71a6bab591e66e95",
  "13f973aaf68a3c82",
  "bac30aa0bebac24f"
 ],
 "1882030798119281410": [
  "eebc9ffbbfcc9f20",
  "95a2cd777c4f7c34",
  "7d09082d1a236499",
  "71a6bab591e66e95",
  "70ae5f5426611f05",
  "bac30aa0bebac24f"
 ],
 "1882030802360772114": [
  "eebc9ffbbfcc9f20",
  "2f58a994c3a0b057",
  "9507b9e8a920594a",
  "71a6bab591e66e95",
  "8c3a0c93469e9f42",
  "bac30aa0bebac24f"
 ],
 "1882030807696985418": [
  "eebc9ffbbfcc9f20",
  "05b1dfda03e06c09",
  "b70eee4f1f6d900d",
  "71a6bab591e66e95",
  "5c92baca663be250",
  "98c3fe1beda6569e"
 ],
 "1882030812480584782": [
  "eebc9ffbbfcc9f20",
  "d00eeedf5c8f1665",
  "ccb445a8e0cc1f2d",
  "71a6bab591e66e95",
  "4a4dff1dd8f08f93",
  "bac30aa0bebac24f"
 ],
 "1882030816821682838": [
  "eebc9ffbbfcc9f20",
  "d961b8bf0210cd3c",
  "3c6b90e1f11a3dd2",
  "71a6bab591e66e95",
  "fed061a3d24ceadc",
  "bac30aa0bebac24f"
 ],
 "1882030821074707868": [
  "eebc9ffbbfcc9f20",
  "493d5d77702687c4",
  "5bd9e6ee99daa9ea",
  "71a6bab591e66e95",
  "92028fe50167039b",
  "984b7311e8ab77bc"
 ],
 "1882030826384706774": [
  "eebc9ffbbfcc9f20",
  "f6a03553ad1596fb",
  "cd738872b22a06fc",
  "71a6bab591e66e95",
  "3595cf3bd46386d5",
  "0052b71e849469e6"
 ],
 "1882030831171448109": [
  "eebc9ffbbfcc9f20",
  "bd5dda7ac9429509",
  "3b1e39891a1f9b81",
  "71a6bab591e66e95",
  "c6d4e3e68a2f5e91",
  "98c3fe1beda6569e"
 ],
 "1882030835495779687": [
  "eebc9ffbbfcc9f20",
  "22978c1eb3ada2b3",
  "1d852cc12f9b862c",
  "71a6bab591e66e95",
  "3e9f7637b528ecc1",
  "0052b71e849469e6"
 ],
 "1882030839808575213": [
  "eebc9ffbbfcc9f20",
  "1323701dd88cddd1",
  "ee4ebca035b624b2",
  "71a6bab591e66e95",
  "8ac95e2683bc056c",
  "bac30aa0bebac24f"
 ],
 "1882030844079420279": [
  "eebc9ffbbfcc9f20",
  "803ad60e5ee598cd",
  "314ac41de04c1079",
  "71a6bab591e66e95",
  "468529d43f9426d6",
  "98c3fe1beda6569e"
 ],
 "1882030848303091331": [
  "eebc9ffbbfcc9f20",
  "38d6fb05ea1f6eda",
  "61f00e7c920b6aae",
  "71a6bab591e66e95",
  "104c12c6d7fb6235",
  "984b7311e8ab77bc"
 ],
 "1882030852539335355": [
  "eebc9ffbbfcc9f20",
  "972c5c179f06bd16",
  "acabbf9d539d903c",
  "71a6bab591e66e95",
  "7ebd55c11a3b2c9c",
  "98c3fe1beda6569e"
 ],
 "1882030857817862148": [
  "eebc9ffbbfcc9f20",
  "5537474ae678cb58",
  "eb2ab3ad2917073d",
  "71a6bab591e66e95",
  "325f5243def62b75",
  "292c9b84a664dd08"
 ],
 "1882030862077178674": [
  "eebc9ffbbfcc9f20",
  "9a1aca8cf36a6292",
  "9dda2f159125ec14",
  "71a6bab591e66e95",
  "41aae4f3fcb43369",
  "0052b71e849469e6"
 ],
 "1882030866842958026": [
  "eebc9ffbbfcc9f20",
  "4fcd75e5858d14b9",
  "a3663d004c7ac657",
  "71a6bab591e66e95",
  "59eac94a851b14e4",
  "bac30aa0bebac24f"
 ],
 "1882030871108567677": [
  "eebc9ffbbfcc9f20",
  "35168f5960d74302",
  "79f4033b2ea8a88c",
  "71a6bab591e66e95",
  "392cede6af1c8a79",
  "98c3fe1beda6569e"
 ],
 "1882030875881686644": [
  "eebc9ffbbfcc9f20",
  "59e9bfcb0c2b0997",
  "31820a22441401a3",
  "71a6bab591e66e95",
  "56ccccdc70d40aa4",
  "bac30aa0bebac24f"
 ],
 "1882030881178036259": [
  "eebc9ffbbfcc9f20",
  "86171f57ee9d38a4",
  "0ab664493eac4a5f",
  "71a6bab591e66e95",
  "34799046153a9479",
  "98c3fe1beda6569e"
 ],
 "1882030885415341833": [
  "eebc9ffbbfcc9f20",
  "1402a80ed7b28b93",
  "03b644eb4b1565e1",
  "71a6bab591e66e95",
  "e8e91b86ebc9b923",
  "bac30aa0bebac24f"
 ],
 "1882030890184257417": [
  "eebc9ffbbfcc9f20",
  "8d5c9b0aa4cbf0ec",
  "f48fa5802c2db5f7",
  "71a6bab591e66e95",
  "16a33ad58dce2735",
  "98c3fe1beda6569e"
 ],
 "1882030895495301172": [
  "eebc9ffbbfcc9f20",
  "e2d5eddbd082280d",
  "c2d4eec84c6c05bf",
  "71a6bab591e66e95",
  "9b92f079db581f5e",
  "bac30aa0bebac24f"
 ],
 "1882030899820677932": [
  "eebc9ffbbfcc9f20",
  "0601258b33ebc971",
  "35419f3c47f3fb3c",
  "71a6bab591e66e95",
  "8ee4348ae0a5abbe",
  "bac30aa0bebac24f"
 ],
 "1882030904043294196": [
  "eebc9ffbbfcc9f20",
  "788b3d14d6726b83",
  "25dbf5d568ce52fb",
  "71a6bab591e66e95",
  "12e0927e57ea320d",
  "bac30aa0bebac24f"
 ],
 "1882030908819553240": [
  "eebc9ffbbfcc9f20",
  "93a1d1e0cf53bc90",
  "2c386f97a68cb2c2",
  "71a6bab591e66e95",
  "8ef447e998933304",
  "98c3fe1beda6569e"
 ],
 "1882030913039025357": [
  "eebc9ffbbfcc9f20",
  "188fd80cd3c79a39",
  "5032efde2554b3f8",
  "71a6bab591e66e95",
  "0ffd874c7849f1ca",
  "bac30aa0bebac24f"
 ],
 "1882030918318597614": [
  "eebc9ffbbfcc9f20",
  "3cae11747f7148b5",
  "d13845e5db345192",
  "71a6bab591e66e95",
  "1082f48cad92c3f8",
  "bac30aa0bebac24f"
 ],
 "1882030923617056899": [
  "eebc9ffbbfcc9f20",
  "0544e1dce14a78e5",
  "dce939447ae0368b",
  "71a6bab591e66e95",
  "b077a77c49f65f03",
  "98c3fe1beda6569e"
 ],
 "1882030928410098633": [
  "eebc9ffbbfcc9f20",
  "da70f9e7a80a55a2",
  "df89f68ff317b0b8",
  "71a6bab591e66e95",
  "89b0e63fc7668cf4",
  "98c3fe1beda6569e"
 ],
 "1882030932718690455": [
  "eebc9ffbbfcc9f20",
  "01b91ecf6533cf0d",
  "0da0eb549a659557",
  "71a6bab591e66e95",
  "86689470f45328b3",
  "292c9b84a664dd08"
 ],
 "1882030937492858007": [
  "eebc9ffbbfcc9f20",
  "4316ef8037342826",
  "b72dff4fdad1af28",
  "71a6bab591e66e95",
  "38fa95620efdb748",
  "98c3fe1beda6569e"
 ],
 "1882030942767196654": [
  "eebc9ffbbfcc9f20",
  "40227056bdde277e",
  "948c15a96dce6ade",
  "71a6bab591e66e95",
  "638076b61aae4a13",
  "98c3fe1beda6569e"
 ],
 "1882030948197776270": [
  "eebc9ffbbfcc9f20",
  "c7ecbcb4b963c9fe",
  "8cd5cbf74b5dabe6",
  "71a6bab591e66e95",
  "b2ae2befbd6ebba8",
  "0052b71e849469e6"
 ],
 "1882030952982421666": [
  "eebc9ffbbfcc9f20",
  "f29f9597f1ce2547",
  "e764bd71498e6c56",
  "71a6bab591e66e95",
  "caae46f8d5116663",
  "98c3fe1beda6569e"
 ],
 "1882030958306052334": [
  "eebc9ffbbfcc9f20",
  "3297a9b54144f3c2",
  "fef3f285deb6c661",
  "71a6bab591e66e95",
  "0b83bba18a7ea1e5",
  "98c3fe1beda6569e"
 ],
 "1882031127298752626": [
  "eebc9ffbbfcc9f20",
  "4d184ed2b22a3542",
  "369ea9b5180c2ef2",
  "7793faeecfea4d6b",
  "02a445958909f7ea",
  "98c3fe1beda6569e"
 ],
 "1882031131570646734": [
  "eebc9ffbbfcc9f20",
  "19f5d65c1f5767ef",
  "f2fc2b4874ef9449",
  "7793faeecfea4d6b",
  "cd4eebb857b1735c",
  "bbcd0238701a15f6"
 ],
 "1882031136871199302": [
  "eebc9ffbbfcc9f20",
  "f1e1bb0951897a8c",
  "643b4be5b26d42d6",
  "7793faeecfea4d6b",
  "1a5eb982ca556ca0",
  "98c3fe1beda6569e"
 ],
 "1882031141725058609": [
  "eebc9ffbbfcc9f20",
  "aea0888733e01ba0",
  "620595b01fbb21bc",
  "7793faeecfea4d6b",
  "a9b6ea26ed79afe7",
  "98c3fe1beda6569e"
 ],
 "1882031146504474549": [
  "eebc9ffbbfcc9f20",
  "f3c8add652105b18",
  "89a73423d51b7d1b",
  "7793faeecfea4d6b",
  "2913051dcfbcbc65",
  "98c3fe1beda6569e"
 ],
 "1882031151284929517": [
  "eebc9ffbbfcc9f20",
  "3d72f0b245c4fcd8",
  "8543499abcb62637",
  "7793faeecfea4d6b",
  "77c31e374b25a42a",
  "bbcd0238701a15f6"
 ],
 "1882031155534809105": [
  "eebc9ffbbfcc9f20",
  "93e3eb7ea44d4630",
  "e073c2dc1f6487f6",
  "7793faeecfea4d6b",
  "54745400595b31b1",
  "98c3fe1beda6569e"
 ],
 "1882031160950705058": [
  "eebc9ffbbfcc9f20",
  "182cceee9153e94d",
  "12516fa7d70e3fc6",
  "7793faeecfea4d6b",
  "8caf20e72667579d",
  "98c3fe1beda6569e"
 ],
 "1882031165724866684": [
  "eebc9ffbbfcc9f20",
  "a733a71e98c8c3ab",
  "6b7baed40e19751c",
  "7793faeecfea4d6b",
  "855296eec9180a17",
  "984b7311e8ab77bc"
 ],
 "1882031171042196656": [
  "eebc9ffbbfcc9f20",
  "12c8481c3e427d22",
  "d5202635dc9f9d9a",
  "7793faeecfea4d6b",
  "592ad782cb2d2417",
  "bbcd0238701a15f6"
 ],
 "1882031176352182339": [
  "eebc9ffbbfcc9f20",
  "7d6586ea51e74e9a",
  "b827f2a89c8c5c61",
  "7793faeecfea4d6b",
  "6f5edf066036dd2b",
  "98c3fe1beda6569e"
 ],
 "1882031180591581492": [
  "eebc9ffbbfcc9f20",
  "0dbae8f7a0b9d116",
  "b685343677a056d1",
  "7793faeecfea4d6b",
  "bf662a2e6624d7f6",
  "98c3fe1beda6569e"
 ],
 "1882031185891076145": [
  "eebc9ffbbfcc9f20",
  "f17586f028879784",
  "59c031d95ac107ee",
  "7793faeecfea4d6b",
  "b48e162d41f4df17",
  "bbcd0238701a15f6"
 ],
 "1882031193395735827": [
  "eebc9ffbbfcc9f20",
  "82fb29d05f5bd977",
  "9537e0099a15a258",
  "7793faeecfea4d6b",
  "a7f007208ded341b",
  "bbcd0238701a15f6"
 ],
 "1882031197621502939": [
  "eebc9ffbbfcc9f20",
  "0cfd057f4f678a1b",
  "78b551482388bf4b",
  "7793faeecfea4d6b",
  "61582dd2c820c275",
  "bbcd0238701a15f6"
 ],
 "1882031201951068745": [
  "eebc9ffbbfcc9f20",
  "543c1fcd2a84df92",
  "cc052876602cef9d",
  "7793faeecfea4d6b",
  "2c7d9e9742a68555",
  "987b536f03aa903c"
 ],
 "1882031206200953830": [
  "eebc9ffbbfcc9f20",
  "8570974c5cbb3efe",
  "f3a18fb1999ab9aa",
  "7793faeecfea4d6b",
  "17985324a11c4155",
  "bbcd0238701a15f6"
 ],
 "1882031211530860906": [
  "eebc9ffbbfcc9f20",
  "4d7e9361c2e2a1a8",
  "000044525db6087a",
  "7793faeecfea4d6b",
  "82f04efdd6775d6d",
  "bbcd0238701a15f6"
 ],
 "1882031216812540574": [
  "eebc9ffbbfcc9f20",
  "e87570db9ee569c0",
  "cb3d349f5dd4d775",
  "7793faeecfea4d6b",
  "d973421b2840f3a1",
  "bbcd0238701a15f6"
 ],
 "1882031222119375569": [
  "eebc9ffbbfcc9f20",
  "69a02cc03c7b0af2",
  "82bb71512b83d08f",
  "7793faeecfea4d6b",
  "9db49d9e5b316fbd",
  "98c3fe1beda6569e"
 ],
 "1882031226942829872": [
  "eebc9ffbbfcc9f20",
  "0a917301ee2cb8ed",
  "8964e002be906c20",
  "7793faeecfea4d6b",
  "b6d780fee5582f1c",
  "98c3fe1beda6569e"
 ],
 "1882031231200055030": [
  "eebc9ffbbfcc9f20",
  "47177d1bb30d515c",
  "8a825ab37f330dd7",
  "7793faeecfea4d6b",
  "e3397c2c6da83d8f",
  "98c3fe1beda6569e"
 ],
 "1882031235952198160": [
  "eebc9ffbbfcc9f20",
  "dc91fa4c278e096c",
  "c1bf471376693e78",
  "7793faeecfea4d6b",
  "a2b2940cf7d3c75d",
  "bbcd0238701a15f6"
 ],
 "1882031240745238462": [
  "eebc9ffbbfcc9f20",
  "28521eab27e83057",
  "083b5676999eb85f",
  "7793faeecfea4d6b",
  "efe9757a244d8880",
  "984b7311e8ab77bc"
 ],
 "1882031245613779252": [
  "eebc9ffbbfcc9f20",
  "30f96c1674c13caa",
  "1c4dea7d1f8eb147",
  "7793faeecfea4d6b",
  "dbcdf5574183dcc9",
  "0052b71e849469e6"
 ],
 "1882031250892306319": [
  "eebc9ffbbfcc9f20",
  "570ba693baffb99d",
  "50681d85ba8450c8",
  "7793faeecfea4d6b",
  "ca70244d5b74f5a7",
  "98c3fe1beda6569e"
 ],
 "1882031255147433964": [
  "eebc9ffbbfcc9f20",
  "1b56485aaf50252c",
  "bd3e0d54c06dc81e",
  "7793faeecfea4d6b",
  "585f9fa445fec7d5",
  "32666181bb749713"
 ],
 "1882031259400449863": [
  "eebc9ffbbfcc9f20",
  "c760d626e80a4508",
  "abe6a5d722a72488",
  "7793faeecfea4d6b",
  "34458547a2ff128f",
  "984b7311e8ab77bc"
 ],
 "1882031264689473155": [
  "eebc9ffbbfcc9f20",
  "b77fe66d122a1799",
  "56a7bb433075ec53",
  "7793faeecfea4d6b",
  "905067f4c0a15a9f",
  "98c3fe1beda6569e"
 ],
 "1882031269494040157": [
  "eebc9ffbbfcc9f20",
  "e1da995d36263a01",
  "b5cfcd41073446d4",
  "7793faeecfea4d6b",
  "2ef6095adf21ac96",
  "bbcd0238701a15f6"
 ],
 "1882031274265065442": [
  "eebc9ffbbfcc9f20",
  "1c77dd73e4daf12f",
  "8b1b8733a40aabd1",
  "7793faeecfea4d6b",
  "ceb7d5f083539d2b",
  "98c3fe1beda6569e"
 ],
 "1882031278608264444": [
  "eebc9ffbbfcc9f20",
  "7f72cf66371bdf06",
  "bce475a473051598",
  "7793faeecfea4d6b",
  "079b2a1537cdd052",
  "bbcd0238701a15f6"
 ],
 "1882031283399214131": [
  "eebc9ffbbfcc9f20",
  "c7efc9337542aa46",
  "a73a47b76da1fe5c",
  "7793faeecfea4d6b",
  "1f789b0c91c88267",
  "984b7311e8ab77bc"
 ],
 "1882031288698718560": [
  "eebc9ffbbfcc9f20",
  "3bcee1d06cd4832d",
  "d1bfd667fc0150f4",
  "7793faeecfea4d6b",
  "685f87cf1325f207",
  "98c3fe1beda6569e"
 ],
 "1882031293999262142": [
  "eebc9ffbbfcc9f20",
  "1a4bcd2f26bffc3b",
  "1c6e1476a161e75e",
  "7793faeecfea4d6b",
  "e742f8c4ace7181c",
  "bbcd0238701a15f6"
 ],
 "1882031299294576749": [
  "eebc9ffbbfcc9f20",
  "07652fc377567352",
  "fdeefbb7a5aa23b0",
  "7793faeecfea4d6b",
  "81d1fe458251e906",
  "bbcd0238701a15f6"
 ],
 "1882031304610858134": [
  "eebc9ffbbfcc9f20",
  "a0a2bb94483f8743",
  "304d3bc1b609a6ff",
  "7793faeecfea4d6b",
  "667326b6aee29fac",
  "bbcd0238701a15f6"
 ],
 "1882031308859679873": [
  "eebc9ffbbfcc9f20",
  "4c81f456fe887e16",
  "1faa5ec6f8a45a0b",
  "7793faeecfea4d6b",
  "b8355c92b0ff848a",
  "51d4d807a6bee023"
 ],
 "1882031521731098214": [
  "eebc9ffbbfcc9f20",
  "f3fdb3d76ff9bb19",
  "0bc8ce4bc0eb85d8",
  "71a6bab591e66e95",
  "4bba0cc52d0b7092",
  "98c3fe1beda6569e"
 ],
 "1882031527095613942": [
  "eebc9ffbbfcc9f20",
  "95a0cbe393e7ef72",
  "1bd48ab9ec0bab2f",
  "71a6bab591e66e95",
  "bcba353b523813c8",
  "bac30aa0bebac24f"
 ],
 "1882031531322426432": [
  "eebc9ffbbfcc9f20",
  "d041319a88095285",
  "133f7a257b5101b0",
  "71a6bab591e66e95",
  "c8f078609fb15a1d",
  "292c9b84a664dd08"
 ],
 "1882031536110220033": [
  "eebc9ffbbfcc9f20",
  "33686584973de0f9",
  "fcd80fe14979bb60",
  "71a6bab591e66e95",
  "845555a6d5a2215c",
  "bac30aa0bebac24f"
 ],
 "1882031541429652402": [
  "eebc9ffbbfcc9f20",
  "e4eafa531de53a1b",
  "ef6b43e43b9676c9",
  "71a6bab591e66e95",
  "4ed1b6c85671f9b8",
  "98c3fe1beda6569e"
 ],
 "1882031546226879350": [
  "eebc9ffbbfcc9f20",
  "064fcb4d3db3ac34",
  "96072c316fc9a483",
  "71a6bab591e66e95",
  "9fb9c0153fa7c377",
  "0052b71e849469e6"
 ],
 "1882031551016779303": [
  "eebc9ffbbfcc9f20",
  "fdd39c6a631eaf14",
  "67c749b1631633ce",
  "71a6bab591e66e95",
  "4d16608d8e6bb993",
  "98c3fe1beda6569e"
 ],
 "1882031555776258786": [
  "eebc9ffbbfcc9f20",
  "ebc78604f046f772",
  "342fa73d8ae9512e",
  "71a6bab591e66e95",
  "b5def1481a50dabb",
  "98c3fe1beda6569e"
 ],
 "1882031561179572181": [
  "eebc9ffbbfcc9f20",
  "2c189c184e3e63fc",
  "ed4ad32c3e28dfdb",
  "71a6bab591e66e95",
  "b419569c6562305d",
  "292c9b84a664dd08"
 ],
 "1882031565467200526": [
  "eebc9ffbbfcc9f20",
  "e9ba6383abd0bf3f",
  "de96421c9b6deda4",
  "71a6bab591e66e95",
  "0f8ef9f191cf39cc",
  "0052b71e849469e6"
 ],
 "1882031569716036257": [
  "eebc9ffbbfcc9f20",
  "bba8f1adc9b1df53",
  "364f567c2074cffb",
  "71a6bab591e66e95",
  "8c1a0e16e01e45f3",
  "bac30aa0bebac24f"
 ],
 "1882031574476563090": [
  "eebc9ffbbfcc9f20",
  "83e489242a693c82",
  "238bfd4809d9c3e5",
  "71a6bab591e66e95",
  "b25874b90de4834e",
  "98c3fe1beda6569e"
 ],
 "1882031579337766055": [
  "eebc9ffbbfcc9f20",
  "9d2e0907031af2a8",
  "2d86d0fdd0934239",
  "71a6bab591e66e95",
  "7361d8ebfbdafc5d",
  "7fba4f9a42d1fdfc"
 ],
 "1882031583601276812": [
  "eebc9ffbbfcc9f20",
  "8d7477c24e98f4df",
  "76bcabf02c4819a1",
  "71a6bab591e66e95",
  "dcf9c962df30a562",
  "98c3fe1beda6569e"
 ],
 "1882031588894489341": [
  "eebc9ffbbfcc9f20",
  "a5a41daa5a57bd62",
  "86eadbbd7dbcac5c",
  "71a6bab591e66e95",
  "b63d9448965718f2",
  "98c3fe1beda6569e"
 ],
 "1882031593131785661": [
  "eebc9ffbbfcc9f20",
  "4067f15bb7aba7ed",
  "7d14815824f45a37",
  "71a6bab591e66e95",
  "3c2f8eddb71061c4",
  "0052b71e849469e6"
 ],
 "1882031597486523847": [
  "eebc9ffbbfcc9f20",
  "b0d853a2a994a289",
  "8bfea26a6a4fa47e",
  "71a6bab591e66e95",
  "450d653427a877af",
  "bac30aa0bebac24f"
 ],
 "1882031601763660566": [
  "eebc9ffbbfcc9f20",
  "245a6e9292a9736c",
  "5b3e420e63064ce4",
  "71a6bab591e66e95",
  "3174a01014ad9465",
  "98c3fe1beda6569e"
 ],
 "1882031607072598261": [
  "eebc9ffbbfcc9f20",
  "4114617df07ada42",
  "b58fecac673e9d2f",
  "71a6bab591e66e95",
  "88318542318a7cc4",
  "bac30aa0bebac24f"
 ],
 "1882031612384694147": [
  "eebc9ffbbfcc9f20",
  "dea1d92b6c1a0aaa",
  "f096dfa224e6cfae",
  "71a6bab591e66e95",
  "8069b89a7df14a41",
  "bac30aa0bebac24f"
 ],
 "1882031617793245980": [
  "eebc9ffbbfcc9f20",
  "8b5455b52010d8ee",
  "22da33c4a7f10048",
  "71a6bab591e66e95",
  "966a8c3fb756142b",
  "bac30aa0bebac24f"
 ],
 "1882031622016905469": [
  "eebc9ffbbfcc9f20",
  "adfe07964a28411d",
  "c9ae4acba841940f",
  "71a6bab591e66e95",
  "515b7909261bebc5",
  "0052b71e849469e6"
 ],
 "1882031626282509706": [
  "eebc9ffbbfcc9f20",
  "254cebec8d93496a",
  "5f4809ce77a691ad",
  "71a6bab591e66e95",
  "90215684a5ec407b",
  "984b7311e8ab77bc"
 ],
 "1882031631589362771": [
  "eebc9ffbbfcc9f20",
  "c2199c76cab9f2b5",
  "62b620cfe57747a9",
  "71a6bab591e66e95",
  "d8236a82f06afa9e",
  "bac30aa0bebac24f"
 ],
 "1882031636888861394": [
  "eebc9ffbbfcc9f20",
  "85ae155bc8bbdc37",
  "bc9e5a357a5ed76f",
  "71a6bab591e66e95",
  "1221f49427cc1cee",
  "98c3fe1beda6569e"
 ],
 "1882031642194656848": [
  "eebc9ffbbfcc9f20",
  "ad790d73c8f39336",
  "55b0b9ebbf29e4aa",
  "71a6bab591e66e95",
  "6098b795ebad89d5",
  "0052b71e849469e6"
 ],
 "1882031646435100237": [
  "eebc9ffbbfcc9f20",
  "8d48762d70052149",
  "1143c5ae2e73332e",
  "71a6bab591e66e95",
  "27268b5f036407ae",
  "0052b71e849469e6"
 ],
 "1882031650783536669": [
  "eebc9ffbbfcc9f20",
  "3be59e6f3db5bb9b",
  "dbe8ca0497b17cad",
  "71a6bab591e66e95",
  "42c2a862453bab4e",
  "98c3fe1beda6569e"
 ],
 "1882031655537790389": [
  "eebc9ffbbfcc9f20",
  "be04f787cd087825",
  "d4464c20c6b98cfd",
  "71a6bab591e66e95",
  "f4d8bd0e3ffb22bb",
  "bac30aa0bebac24f"
 ],
 "1882031659797103080": [
  "eebc9ffbbfcc9f20",
  "3f28fe40af2d854b",
  "4afe37d02019a4e8",
  "71a6bab591e66e95",
  "343744e486ccd474",
  "bac30aa0bebac24f"
 ],
 "1882031664046973463": [
  "eebc9ffbbfcc9f20",
  "7a255df56594594d",
  "9fd382624678b865",
  "71a6bab591e66e95",
  "d049a68591489535",
  "bac30aa0bebac24f"
 ],
 "1882031668378645531": [
  "eebc9ffbbfcc9f20",
  "828394ff14f5dbe8",
  "4fbd129b63a23170",
  "71a6bab591e66e95",
  "c9fd6643e3ae1d34",
  "bac30aa0bebac24f"
 ],
 "1882031673689689419": [
  "eebc9ffbbfcc9f20",
  "a94a34711399d521",
  "1a006592385b9c44",
  "71a6bab591e66e95",
  "fb8ab5c5082f8fb5",
  "bac30aa0bebac24f"
 ],
 "1882031677938514899": [
  "eebc9ffbbfcc9f20",
  "f4706b004001d08a",
  "836f72410937569e",
  "71a6bab591e66e95",
  "908164a7117a7648",
  "98c3fe1beda6569e"
 ],
 "1882031682155888360": [
  "eebc9ffbbfcc9f20",
  "a41f2d503ab2fc8f",
  "cb80c768c2f2c999",
  "71a6bab591e66e95",
  "c0cd8fa0fca0a38f",
  "98c3fe1beda6569e"
 ],
 "1882031687461676255": [
  "eebc9ffbbfcc9f20",
  "09a2341d525ad11f",
  "7c497d0eed37a089",
  "71a6bab591e66e95",
  "9877a5a6f847448d",
  "bac30aa0bebac24f"
 ],
 "1882031691728332752": [
  "eebc9ffbbfcc9f20",
  "d7b1b56b62b200cd",
  "f24e24c049f4f4ce",
  "71a6bab591e66e95",
  "c001d7d160795a1c",
  "bac30aa0bebac24f"
 ]
};
  const s = (v) => (v === null || v === undefined) ? '' : String(v);
  const groups = (d) => { const b = d.betLog, sd = d.seedHistory, gv = b.gv, bv = b.bv || {};
    const vp = d.gameUnique === 'video-poker';
    const sel = vp ? [s(bv.suggest), (gv.holdHard || []).map(s).join(',')]
                   : [(bv.betData || []).map(x => s(x.type) + ':' + s(x.betAmount)).join(';')];
    const cards = vp ? [(gv.initialHard || []).map(s).join(','), (gv.playerHard || []).map(s).join(',')]
                     : [gv.players.map(s).join(','), gv.bankers.map(s).join(','), s(gv.playerPoint), s(gv.bankerPoint)];
    return {game: [s(d.gameUnique), s(d.gameName)], bet: [s(b.distributeId), s(b.currencyName), s(b.betTime)],
            seeds: [s(sd.serverSeed), s(sd.serverSeedHash), s(sd.clientSeed), s(b.nonce)], selection: sel, cards: cards,
            money: [s(b.betAmount), s(b.winAmount)]}; };
  const sha = async (t) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t))))
    .map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 16);
  const lines = []; let same = 0;
  for (const [id, want] of Object.entries(expected)) {
    let line;
    try {
      const j = await (await fetch('/api/game/bet/v2/bet/' + id, {credentials: 'omit'})).json();
      if (!j || !j.data) line = id + '  no record';
      else {
        const g = groups(j.data), differ = [];
        for (let i = 0; i < GROUPS.length; i++) if (await sha(g[GROUPS[i]].join('|')) !== want[i]) differ.push(GROUPS[i]);
        if (!differ.length) same++;
        line = id + '  ' + j.data.gameUnique + '  ' + (differ.length ? 'differs: ' + differ.join(', ') : 'same: ' + GROUPS.join(', '));
      }
    } catch (e) { line = id + '  error ' + e; }
    lines.push(line);
    await new Promise(res => setTimeout(res, 150));
  }
  const total = 'BC public records matching this package: ' + same + ' of ' + Object.keys(expected).length;
  console.log(lines.join('\n') + '\n' + total);
  return total;
})();
