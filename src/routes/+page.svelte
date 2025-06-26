<script>
  import Header from '../components/Header.svelte';
  export let data;

  const { imdbCSV } = data;
</script>

<Header {imdbCSV} />