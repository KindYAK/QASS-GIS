<template>
  <div class="text-justify pl-10 pr-10">
    <div class="text-h4 mb-5">
      Архив данных по Южно-Казахстанской Области
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}2003 Узыната.DOC`'>2003 Узыната</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}cо жамбыл 2006 МАхтаарал.doc`'>СО жамбыл 2006 Махтаарал</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Достык шард Галым 2005.doc`'>Достык шард Галым 2005</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Жылысу2005.doc`'>Жылысу2005</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Ииржар 2006.doc`'>Ииржар 2006</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Казахстан.doc`'>Казахстан</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Кзылкум2006.doc`'>Кзылкум2006</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Коксу.doc`'>Коксу</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Коссеит.doc`'>Коссеит</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}Нурлыбаева 2006.doc`'>Нурлыбаева 2006</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}с.о Казыбекби Мактаарал Камбаров Г.doc`'>С.о. Казыбекби Мактаарал Камбаров Г</a>
    </div>

    <div class="text-body-1 mb-5">
      <a :href='`${MEDIA_URL}со Достык.doc`'>СО Достык</a>
    </div>
  </div>
</template>

<script>
import {MEDIA_URL} from '~/settings/settings'

export default {
  data() {
    return {
      MEDIA_URL: MEDIA_URL
    }
  },
  methods: {
  }
}
</script>
