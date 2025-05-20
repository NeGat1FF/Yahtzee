<template>
  <div class="container">
    <div class="dice">
      <h2>Dice</h2>
      <img v-for="(val, idx) in dice" :key="idx" :src="diceImages[val]" class="dice-icon" />
    </div>

    <div v-if="isRolling" class="rolling-popup">
      Rolling<span class="dots"></span>
    </div>

    <div class="bottom">
      <div class="left">
        <div class="combinations">
          <h1 style="text-align: center;">Prices</h1>
          <div v-for="(multiplier, name) in combinations" :key="name" class="combo-row">
            <h2 class="combo-name" :style="{ color: name === winningCombo ? '#22c55e' : 'inherit' }">{{ name }}</h2>
            <h2 class="combo-multiplier" style="font-weight: bold;">x{{ multiplier.toFixed(2) }}</h2>
          </div>
        </div>
      </div>

      <div class="right">
        <div class="bet">
          <h2>Bet</h2>
          <div class="input-group">
            <input type="number" placeholder="1" v-model="betAmount"/>
            <button @click="rollDice">Roll</button>
          </div>
        </div>

        <div class="balance">
          <h2>Balance</h2>
          <h1 style="font-weight: bold;">{{ balance }}</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const diceImages = {
  1: new URL('@/assets/dice/dice-1.svg', import.meta.url).href,
  2: new URL('@/assets/dice/dice-2.svg', import.meta.url).href,
  3: new URL('@/assets/dice/dice-3.svg', import.meta.url).href,
  4: new URL('@/assets/dice/dice-4.svg', import.meta.url).href,
  5: new URL('@/assets/dice/dice-5.svg', import.meta.url).href,
  6: new URL('@/assets/dice/dice-6.svg', import.meta.url).href,
};



const balance = ref(100);
const betAmount = ref(0);
const combinations = ref({});
const dice = ref([6, 6, 6, 6, 6, 6])
const isRolling = ref(false);
const winningCombo = ref();


async function fetchCombinations() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/combinations');
    const data = await res.json();
    combinations.value = data;
  } catch (err) {
    console.error('Failed to load combinations:', err);
  }
}

async function fetchBalance() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/balance');
    const data = await res.json();
    balance.value = data.balance;
  } catch (err) {
    console.error('Failed to fetch balance:', err);
  }

}

async function rollDice() {
  try {
    isRolling.value = true;
    balance.value -= betAmount.value;

    await new Promise(resolve => setTimeout(resolve, 1200));


    const res = await fetch('http://127.0.0.1:8000/api/v1/bet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: betAmount.value }),
    });
    const data = await res.json();
    dice.value = data.dice;
    winningCombo.value = data.result;
    console.log(data)
    isRolling.value = false;
    fetchBalance();
  } catch (err) {
    console.error('Failed to roll dice:', err);
  }
}

onMounted(() => {
  fetchCombinations();
  fetchBalance();
});
</script>
