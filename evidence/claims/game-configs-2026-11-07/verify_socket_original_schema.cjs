// Independent decoding of saved raw socket frames using captured public code.
// No network activity. Existing captures are never modified.
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const dir=__dirname,prior=path.join(dir,'source_dependencies');
const paths={runtime:path.join(prior,'bc_current_games_manifest.js'),schema:path.join(prior,'bc_current_GamePageData-BHVZh_Si.js'),socket:path.join(prior,'bc_current_index.js'),labels:path.join(prior,'bc_current_vp_index-CLrD9Klk.js')};
const src=Object.fromEntries(Object.entries(paths).map(([k,p])=>[k,fs.readFileSync(p,'utf8')]));
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const runtime=src.runtime.slice(src.runtime.indexOf('var cn='),src.runtime.indexOf('se.configure();')+'se.configure();'.length);
const a=src.schema.indexOf('const Sn=T.Reader'),i=src.schema.indexOf('const dT=qt.Init=',a),z=src.schema.indexOf('})();',i)+5;
const schema=src.schema.slice(a,z);
const pa=src.socket.indexOf('function YC('),pz=src.socket.indexOf('const h3=',pa);
const parser=src.socket.slice(pa,pz);
const ea=src.socket.indexOf('Qg=Wr.Reader'),ez=src.socket.indexOf('tx=()=>ya',ea);
const envelope='const '+src.socket.slice(ea,ez).replace(/,$/,';');
// G is the optional Long implementation. null selects the runtime's native
// number fallback. All relevant GameConfig numeric fields are 32-bit.
const context=vm.createContext({Uint8Array,ArrayBuffer,DataView,TextDecoder,TextEncoder,Buffer,G:null});
vm.runInContext(runtime+'\nconst T=se,Wr=se,Zg=new TextDecoder;'+schema+'\n'+envelope+'\n'+parser+'\nglobalThis.original={parse:YC,envelope:ex,init:dT};',context);
const labels={9:'Royal flush',8:'Straight flush',7:'Four of a kind',6:'Full house',5:'Flush',4:'Straight',3:'Three of a kind',2:'Two pairs',1:'Jacks or better',0:'No win'};
const files=fs.readdirSync(dir).filter(n=>/^socket_init_g_vp_.*\.json$/.test(n)).sort();
const results=files.map(name=>{
 const raw=fs.readFileSync(path.join(dir,name)),capture=JSON.parse(raw),frames=capture.frames||[];
 const answer={file:name,captureSha256:sha(raw),startedAt:capture.startedAt,namespace:capture.namespace,probeError:capture.error};
 const outgoing=frames.filter(f=>f.direction==='out').map(f=>f.operation);
 answer.outgoingOperations=outgoing;answer.onlyConnectAndInit=outgoing.every(x=>x==='namespace connect'||x==='init');
 for(const f of frames)if(f.direction==='in'&&f.base64){
  const bytes=Buffer.from(f.base64,'base64');if(bytes[0]!==4)continue;
  const body=Uint8Array.from(bytes.subarray(1));const packet=context.original.parse(body.buffer);
  if(packet.namespace!==capture.namespace||(packet.type!==3&&packet.type!==6)||packet.ackId!==0)continue;
  const result=context.original.envelope.decode(new Uint8Array(packet.data));
  answer.resultCode=result.code;answer.resultMessage=result.msg;
  if(result.code===0){const init=context.original.init.decode(result.data);answer.payloadSha256=sha(result.data);
   answer.gameConfig=init.gameConfig.map(row=>{const table=row.payTable?JSON.parse(row.payTable):null;return{gameName:row.gameName,namespace:row.gameSocketNameSpace,version:row.version,rtp:row.rtp,isSingle:row.isSingle,isDelete:row.isDelete,payTable:table,orderedPaytable:table?[9,8,7,6,5,4,3,2,1].map(k=>table[k]):null,rows:table?Object.entries(labels).map(([k,label])=>({index:Number(k),label,payout:table[k]})):null};});
   answer.payoutStringsAgreeWithProbe=answer.gameConfig.every((r,j)=>JSON.stringify(r.payTable)===JSON.stringify(JSON.parse(capture.init.gameConfig[j].payTable)));
  }
 }
 return answer;
});
const report={method:'Exact captured public custom socket parser, ResultObj protobuf decoder, and SingleGame.Init/GameConfig protobuf decoders; raw received frames independently decoded. No network.',sources:Object.fromEntries(Object.entries(paths).map(([k,p])=>[k,{path:path.relative(dir,p),sha256:sha(fs.readFileSync(p))}])),extractedCodeSha256:{runtime:sha(runtime),schema:sha(schema),envelope:sha(envelope),parser:sha(parser)},longConfiguration:'Optional Long implementation is null; runtime uses native numeric fallback. Relevant fields are strings,32-bit integers and booleans.',labelMappingExtractedFromSource:[...src.labels.matchAll(/label:c\("([^"]+)"\),oddIndex:(\d+)/g)].map(m=>({label:m[1],index:Number(m[2])})),versionCorrection:'Initial probe captures stored raw protobuf varints for version. Public schema declares sint32, so raw4 is version2 and raw6 is version3. Raw originals are retained unchanged; this report gives correctly decoded values.',results};
fs.writeFileSync(path.join(dir,'socket_original_schema_verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(results.map(r=>({file:r.file,namespace:r.namespace,error:r.probeError,code:r.resultCode,gameConfig:r.gameConfig,onlyConnectAndInit:r.onlyConnectAndInit})),null,2));
