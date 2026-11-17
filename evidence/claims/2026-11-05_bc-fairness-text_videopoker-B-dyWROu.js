(function(){try{var e=typeof window!="undefined"?window:typeof global!="undefined"?global:typeof globalThis!="undefined"?globalThis:typeof self!="undefined"?self:{};e.SENTRY_RELEASE={id:"1891a0d9b090c8948d242b30bc3f8053271a31ac"},e._sentryModuleMetadata=e._sentryModuleMetadata||{},e._sentryModuleMetadata[new e.Error().stack]=(function(t){for(var a=1;a<arguments.length;a++){var n=arguments[a];if(n!=null)for(var s in n)n.hasOwnProperty(s)&&(t[s]=n[s])}return t})({},e._sentryModuleMetadata[new e.Error().stack],{"_sentryBundlerPluginAppKey:playsmart-ai":!0,release:"1891a0d9b090c8948d242b30bc3f8053271a31ac",dsn:"https://5ea349d46eb7979c2d67abc6db4fb0b3@o4507871583338496.ingest.us.sentry.io/4511183146844160"})}catch(t){}})();const i=`<div class="item">
  <h2>Solving the Trust Issue with Online Gambling</h2>
  <div class="help-content">
    <p>
      The underlying concept of provable fairness is that players have the
      ability to prove and verify that their results are fair and
      unmanipulated. This is achieved through the use of a commitment
      scheme, along with cryptographic hashing.
    </p>
    <p>
      The commitment scheme is used to ensure that the player has an
      influence on all results generated. Cryptographic hashing is used to
      ensure that the casino also remains honest to this commitment
      scheme. Both concepts combined creates a trust-less environment when
      gambling online.
    </p>
  </div>
  <h2>This is simplified in the following representation: </h2>
  <div class="help-content">
    <p>Hex string: hash = HMAC_SHA512(clientSeed:nonce, serverSeed)</p>
    <p>Shuffling logic:</p>
    <ol>
      <li>
        Create a deck of cards named ß, the card is sequenced as spade
        A-K, heart A-K, club A-K and diamond A-K.
      </li>
      <li>
        Use combination to get the hash value, which will be used as the
        weight of the first card (spade A) in the card ß.
      </li>
      <li>
        Delete the first bit of the hash value and add it back as the last
        character of the hash value (for example 54321 to 43215), the new
        hash value will be used as the weight of the second card of ß
        (Spades 2).
      </li>
      <li>Repeat step 2 to calculate the weight for all the card in ß</li>
      <li>
        Finally, shuffle ß according to the corresponding weights of the
        cards, from small to large. The reordered cards is the shuffled ß.
      </li>
    </ol>
    <p>
      Note: A new seed must be set to verify the previous data (the server
      seed is encrypted)
    </p>
  </div>
</div>`;export{i as default};
